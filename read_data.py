import struct

in_sync=0

event={
    'evt_number':0,
    'evt_time':0,
    'e16':0
}

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input', default='raw_data.dat')
parser.add_argument('--output', default='dataTree.root')

args = parser.parse_args()

import ROOT as R
## A C/C++ structure is required, to allow memory based access
R.gROOT.ProcessLine(
"struct event_t {\
   UInt_t          evt_number;\
   Float_t          evt_time;\
   UInt_t          e16;\
};" );

evt=R.event_t()


fOut=R.TFile(args.output,"RECREATE")
t=R.TTree('dataTree','PETIROC data')
t.Branch('evt_number', R.addressof(evt,'evt_number')  ,'evt_number/I')
t.Branch('evt_time',   R.addressof(evt,'evt_time')    ,'evt_time/F')
t.Branch('e16',        R.addressof(evt,'e16')         ,'e16/I')

print("Opening %s"%args.input)
nevents=0
try:
    with open(args.input, "rb") as f:
        while True:
            # Do stuff with byte.
            word = f.read(4)
            if len(word)<4:
                break
            data=struct.unpack('I',word)[0]
            #print('%x'%data)
            if (in_sync==1):
                event['evt_number']=data
                in_sync+=1
            elif (in_sync==2):
                event['evt_time']=data<<32
                in_sync+=1
            elif (in_sync==3):
                event['evt_time']+=data
                event['evt_time']=event['evt_time']*6.25/1e9 #time in second
                in_sync+=1
            elif (in_sync==4):
                event['e16']=(data>>16)
                in_sync+=1
            elif (in_sync==5):
                if(int(data)!=7):
                    print('Corrupted data. Skipping event')
                    in_sync==0
                else:
                    in_sync+=1

            if (data==0x08000000 and in_sync==0):
            #    print("BOE")
                in_sync=1
            if (data==0x08000001 and in_sync==6):
                #print(event)
                evt.evt_number=event['evt_number']
                evt.evt_time=event['evt_time']
                evt.e16=event['e16']
                t.Fill()
                nevents+=1
                if (nevents%1000==0):
                    print("Reading event %d"%nevents,end='\r',flush=True)
                in_sync=0
    t.Print()
    fOut.Write()
except IOError:
     print('\nError While Opening the file!')
