from Digital_Functions import *
from ctypes import *
import matplotlib.pyplot as plt
import time
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='raw_data.dat')
parser.add_argument('--nevents', type=int, default=1000)
parser.add_argument('--timing_mode', action="store_true")
parser.add_argument('--hv', type=float, default=57)
parser.add_argument('--thr', type=int, default=174)
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

if (not args.timing_mode):
        print("Energy mode (no ToT). Readout rate limited to about 50 kHz")
        config_bit="000000000000000000000000000000000000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000011111111111111110111111111111111000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001110000011000"+bin(args.thr)[2:2+11].zfill(10)+"110011110000101011111111111111111010111111111001111111111111001001"
else:
        print("Timing (non latched) mode. Energy measurement unavailable only ToT")
        #Non Latched (mask all but ch16)
        config_bit="000000000000000000000000000000000000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000110000000011111111111111110111111111111111000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001000001110000011000"+bin(args.thr)[2:2+11].zfill(10)+"110011110000101011111111101111111010111111111001111111111111001001"

print("Config bitstream size %d"%len(config_bit))
PETIROC_PetirocCfg0_CONFIG(config_bit,handle)
time.sleep(1)

## ---------------------------------------------------- ##
## HV CONTROLLER                                        ##
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
if (not args.timing_mode):
        err+=REG_rej_en_SET(0, handle)
else:
        err+=REG_rej_en_SET(1, handle)
#max rate 1MHz         
err+=REG_rej_delay_SET(50, handle)
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

N_Packet = 100
Timeout_ms = 50
N_Total_Events = args.nevents
ReadDataNumber = 0
FrameSize=7
if (CPACK_CP_0_START(handle) == True):
	print("Start run")
	time.sleep(0.1)
	err=REG_tr_en_SET(1, handle)
	counts=0
	[err, Frame_Status] = CPACK_CP_0_GET_STATUS(handle)
	if (Frame_Status >0):
		while( counts < N_Total_Events):
			try:
				[err, Frame_Data, Frame_Read_Data, Frame_Valid_Data] = CPACK_CP_0_GET_DATA(N_Packet, Timeout_ms, handle)
				read_data=(c_uint * int(Frame_Valid_Data.value)).from_address(addressof(Frame_Data))
				out_raw.write(read_data)

				#[Time_Code, Pack_Id, Energy] = CPACK_CP_0_RECONSTRUCT_DATA(Frame_Data)
				ReadDataNumber += int(Frame_Valid_Data.value) #total number of words
				[err,counts]=REG_dv_tot_GET(handle)

				print("Event Id: %d(%d)/%d"%(counts,ReadDataNumber/FrameSize,N_Total_Events), end='\r',flush=True)
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
