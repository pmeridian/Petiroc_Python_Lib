from Digital_Functions import *
from ctypes import *
import matplotlib.pyplot as plt
import time
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='raw_data.dat')
parser.add_argument('--nevents', type=int, default=1000)
parser.add_argument('--hv', type=float, default=57)
args = parser.parse_args()

def stop_running():
	#print("\nException: ",e)
	print("Stop Run")
	err=REG_tr_en_SET(0, handle)
	print("Closing file %s"%args.output)
	out_raw.close()

	[err, enable, voltage, current] = GetHV_A7585D(handle)
	SetHV_A7585D(0,0,handle)
	while abs(voltage) > 20:
		[err, enable, voltage, current] = GetHV_A7585D(handle)
		print("%d: %.2f V %.3f muA"%(enable, voltage, current*1e3))
		time.sleep(1)
	print("HV OFF")
	exit(0)

[ListOfDevices, count] = ListDevices()
if (count > 0):

	board = ListOfDevices[0].encode('utf-8')

	Init()
	[err, handle] = ConnectDevice(board)
	if (err == 0):
		print("Successful connection to board ", board)
	else:
		print("Connection Error")
		exit(-1)

print("Config PETIROC")
PETIROC_PetirocCfg0_CONFIG("0000000000000000000000000000000000000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000001100000000000000000000000000000000000000000000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000010000011100000110000010101110110011110000101011111111111111111010111111111001111111111111001001",handle)
time.sleep(1)

## ---------------------------------------------------- ##
## CODE EXAMPLE FOR HV CONTROLLER                       ##
SetIICControllerBaseAddress(Digital_RegisterFile.SCI_REG_i2chv_CTRL, Digital_RegisterFile.SCI_REG_i2chv_MON, handle)
voltage=0
target_voltage=args.hv
SetHV_A7585D(1,target_voltage,handle)
while abs(voltage-target_voltage) > 0.2:
	[err, enable, voltage, current] = GetHV_A7585D(handle)
	print("%d: %.2f V %.3f muA"%(enable, voltage, current*1e3))
	time.sleep(1)

print("HV ON")
time.sleep(1)
## ---------------------------------------------------- ##
#   config board & reset counters
err=REG_tr_en_SET(0, handle)
time.sleep(0.1)
err+=REG_run_start_SET(0, handle)
err+=REG_tr_sel_SET(0, handle)
err+=REG_sw_trig_freq_SET(0, handle)
[err,counts]=REG_c_tot_GET(handle)

if (err):
	print("Config error")
	exit(-1)
if (counts>0):
	print("Reset error")
	exit(-1)
if (CPACK_CP_0_RESET(handle) != 0):
	print("Reset Error!")
	exit(-1)

#plt.ion()
#plt.show()
print("Writing data to %s"%args.output)
out_raw=open(args.output, "wb")

N_Packet = 50
Timeout_ms = 1000
N_Total_Events = args.nevents
ReadDataNumber = 0
if (CPACK_CP_0_START(handle) == True):
	print("Start run")
	time.sleep(0.1)
	err=REG_tr_en_SET(1, handle)
	counts=0
	[err, Frame_Status] = CPACK_CP_0_GET_STATUS(handle)
	if (Frame_Status >0):
		while( int(ReadDataNumber)/7 < N_Total_Events):
			try:
				[err, Frame_Data, Frame_Read_Data, Frame_Valid_Data] = CPACK_CP_0_GET_DATA(N_Packet, Timeout_ms, handle)
				read_data=(c_uint * int(Frame_Valid_Data.value)).from_address(addressof(Frame_Data))
				out_raw.write(read_data)

				#[Time_Code, Pack_Id, Energy] = CPACK_CP_0_RECONSTRUCT_DATA(Frame_Data)
				ReadDataNumber += int(Frame_Valid_Data.value) #total number of words
				[err,counts]=REG_dv_tot_GET(handle)

				print("Event Id: %d(%d)/%d"%(ReadDataNumber/7,counts,N_Total_Events), end='\r',flush=True)
			except KeyboardInterrupt:
				print("")
				stop_running()
			#plt.cla()
			#plt.plot(Energy[0])
			#plt.pause(0.01)
	else:
		print("Status Error")
		exit(-1)
else:
	print("Start Error")
	exit(-1)

stop_running()
