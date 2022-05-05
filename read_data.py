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
args = parser.parse_args()

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
                    print('Corrupted data')
                    break
                in_sync+=1

            if (data==0x08000000):
            #    print("BOE")
                in_sync=1
            if (data==0x08000001):
                print(event)
                in_sync=0

except IOError:
     print('Error While Opening the file!')
