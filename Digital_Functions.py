









import Digital_RegisterFile
from ctypes import *
import array
import numpy as np

import os

mydll = cdll.LoadLibrary(os.path.dirname(__file__) +'/niusb3_core.dll')

def Init():
    err = mydll.NI_USB3_Init()
    return err

def ConnectDevice(board):
    handle = c_void_p(256)
    err = mydll.NI_USB3_ConnectDevice(board, byref(handle))
    return err, handle

def CloseConnect(handle):
    err = mydll.NI_USB3_CloseConnection(byref(handle))
    return err

def ListDevices():
    count = c_int(0)
    s = create_string_buffer(2048)
    err = mydll.NI_USB3_ListDevices(byref(s), 0, byref(count))
    str_con = (s.value.decode('ascii'))
    str_devices = str_con.split(';')
    dev_count = count.value
    return str_devices, dev_count

def __abstracted_reg_write(data, address, handle):
    err = mydll.NI_USB3_WriteReg(data, address, byref(handle))
    return err

def __abstracted_reg_read(address, handle):
    data = c_uint(0)
    err = mydll.NI_USB3_ReadReg(byref(data), address, byref(handle))
    return err, data.value

def __abstracted_mem_write(data, count, address, timeout_ms, handle):
    written_data = c_uint(0)
    err = mydll.NI_USB3_WriteData(data, count, address, 0, timeout_ms, byref(handle), byref(written_data))
    return err, written_data.value

def __abstracted_mem_read(count, address, timeout_ms, handle):
    data = (c_uint * (2* count))()
    read_data = c_uint(0)
    valid_data = c_uint(0)
    err = mydll.NI_USB3_ReadData(byref(data), count, address, 0, timeout_ms, byref(handle), byref(read_data), byref(valid_data))
    return err, data, read_data.value, valid_data.value

def __abstracted_fifo_write(data, count, address, timeout_ms, handle):
    written_data = c_uint(0)
    err = mydll.NI_USB3_WriteData(data, count, address, 1, timeout_ms, byref(handle), byref(written_data))
    return err, written_data.value

def __abstracted_fifo_read(count, address, address_status, blocking, timeout_ms, handle):
    data = (c_uint * (2 * count))()
    #data = (c_uint * (count))()
    read_data = c_uint(0)
    valid_data = c_uint(0)
    err = mydll.NI_USB3_ReadData(byref(data), count, address, 1, timeout_ms, byref(handle), byref(read_data), byref(valid_data))
    return err, data, read_data, valid_data

#def SetAFEBaseAddress(handle):
#    err = mydll.NI_USB3_SetIICControllerBaseAddress(Digital_RegisterFile.SCI_AFE_REG_CTRL, Digital_RegisterFile.SCI_AFE_REG_MON, byref(handle))
#    return err

def SetAFEOffset(top, value, handle):
    err = mydll.NI_USB3_SetOffset(top, value, byref(handle))
    return err

def SetAFEImpedance(value, handle):
    err = mydll.NI_USB3_SetImpedance(value, byref(handle))
    return err

def SetIICControllerBaseAddress(reg_cntrl, reg_mon, handle):
    err = mydll.NI_USB3_SetIICControllerBaseAddress(reg_cntrl, reg_mon, byref(handle))
    return err

def SetHV_A7585D(enable, voltge, handle):
    err = mydll.NI_USB3_SetHV(enable, c_float(voltge), byref(handle))
    return err

def GetHV_A7585D(handle):
    enable = c_int(0)
    voltage = c_float(0)
    current = c_float(0)
    err = mydll.NI_USB3_GetHV(byref(enable), byref(voltage), byref(current), byref(handle))
    return err, enable.value, voltage.value, current.value

def gray_to_bin(num, nbit):
	temp = num ^ (num >> 8)
	temp ^= (temp >> 4)
	temp ^= (temp >> 2)
	temp ^= (temp >> 1)
	return temp

def REG_c_tot_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_c_tot, handle)
    return err, data

def REG_c_tot_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_c_tot, handle)
    return err

def REG_run_time_lsb_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_run_time_lsb, handle)
    return err, data

def REG_run_time_lsb_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_run_time_lsb, handle)
    return err

def REG_run_time_msb_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_run_time_msb, handle)
    return err, data

def REG_run_time_msb_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_run_time_msb, handle)
    return err

def REG_run_start_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_run_start, handle)
    return err, data

def REG_run_start_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_run_start, handle)
    return err

def REG_sw_trig_freq_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_sw_trig_freq, handle)
    return err, data

def REG_sw_trig_freq_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_sw_trig_freq, handle)
    return err

def REG_tr_sel_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_tr_sel, handle)
    return err, data

def REG_tr_sel_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_tr_sel, handle)
    return err

def REG_e16_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_e16, handle)
    return err, data

def REG_e16_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_e16, handle)
    return err

def REG_evt_ts_msb_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_evt_ts_msb, handle)
    return err, data

def REG_evt_ts_msb_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_evt_ts_msb, handle)
    return err

def REG_evt_ts_lsb_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_evt_ts_lsb, handle)
    return err, data

def REG_evt_ts_lsb_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_evt_ts_lsb, handle)
    return err

def REG_e15_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_e15, handle)
    return err, data

def REG_e15_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_e15, handle)
    return err

def REG_tr_en_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_tr_en, handle)
    return err, data

def REG_tr_en_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_tr_en, handle)
    return err

def REG_fw_ver_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_fw_ver, handle)
    return err, data

def REG_fw_ver_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_fw_ver, handle)
    return err

def REG_dv_tot_GET(handle):
    [err, data] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_dv_tot, handle)
    return err, data

def REG_dv_tot_SET(data, handle):
    err = __abstracted_reg_write(data, Digital_RegisterFile.SCI_REG_dv_tot, handle)
    return err




def CPACK_CP_0_RESET(handle):
	err = __abstracted_reg_write(2, Digital_RegisterFile.SCI_REG_CP_0_CONFIG, handle)
	err = __abstracted_reg_write(0, Digital_RegisterFile.SCI_REG_CP_0_CONFIG, handle)
	return err

def CPACK_CP_0_FLUSH(handle):
	err = __abstracted_reg_write(4, Digital_RegisterFile.SCI_REG_CP_0_CONFIG, handle)
	err = __abstracted_reg_write(0, Digital_RegisterFile.SCI_REG_CP_0_CONFIG, handle)
	return err

def CPACK_CP_0_START(handle):
	err = __abstracted_reg_write(2, Digital_RegisterFile.SCI_REG_CP_0_CONFIG, handle)
	if (err != 0):
	   return False
	err = __abstracted_reg_write(0, Digital_RegisterFile.SCI_REG_CP_0_CONFIG, handle)
	if (err != 0):
	   return False
	err = __abstracted_reg_write(1, Digital_RegisterFile.SCI_REG_CP_0_CONFIG, handle)
	if (err != 0):
	   return False
	return True

def CPACK_CP_0_GET_STATUS(handle):
	[err, status] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_CP_0_READ_STATUS, handle)
	status = status & 0xf
	return err, status

def CPACK_CP_0_GET_AVAILABLE_DATA(handle):
	[err, status] = __abstracted_reg_read(Digital_RegisterFile.SCI_REG_CP_0_READ_VALID_WORDS, handle)
	return err, status

def CPACK_CP_0_GET_DATA(n_packet, timeout_ms, handle):
	data_length = n_packet *( 7 )
	[err, data, read_data, valid_data] = __abstracted_fifo_read(data_length, Digital_RegisterFile.SCI_REG_CP_0_FIFOADDRESS, Digital_RegisterFile.SCI_REG_CP_0_READ_STATUS, True, timeout_ms, handle)
	return err, data, read_data, valid_data


def CPACK_CP_0_RECONSTRUCT_DATA(FrameData):
	in_sync = 0
	tot_data = len(FrameData)
	n_ch = 7
	n_packet = tot_data / (7)
	event_energy, Time_Code, Pack_Id, Energy = ([] for i in range(4))
	for i in range(len(FrameData)):
		mpe = FrameData[i]
		if (in_sync == 0):
			if (mpe != 0x0800000):
				continue
			in_sync = 1
			continue
		if (in_sync == 1):
			event_timecode = mpe
			Time_Code.append(event_timecode)
			in_sync = 2
			continue
		if (in_sync == 2):
			Pack_Id.append(mpe)
			in_sync = 3
			ch_index = 0
			continue
		if (in_sync == 3):
			if (mpe == 0x0800000):
				in_sync = 1
			else:
				ev_energy = mpe
				event_energy.append(ev_energy)
				ch_index += 1
				if (ch_index == n_ch):
					Energy.append(event_energy)
					event_energy = []
					in_sync = 0
	return Time_Code, Pack_Id, Energy


def RATE_METER_RateMeter_0_GET_DATA(channels, timeout_ms, handle):
    [err, data, read_data, valid_data] = __abstracted_mem_read(channels, Digital_RegisterFile.SCI_REG_RateMeter_0_FIFOADDRESS, timeout_ms, handle)
    return err, data, read_data, valid_data




def RATE_METER_RateMeter_0_GET_DATA_COUNTS(channels, timeout_ms, handle):
    [err, data, read_data, valid_data] = __abstracted_mem_read(channels, Digital_RegisterFile.SCI_REG_RateMeter_0_FIFOADDRESS + 512, timeout_ms, handle)
    return err, data, read_data, valid_data




def PETIROC_PetirocCfg0_CONFIG(incfg, handle):
	bitstream = array.array('I',(0 for i in range(0,1024)))
	cfg = array.array('I',(0 for i in range(0,20)))
	bitstream_str = np.fromstring(incfg,'u1') - ord('0')
	for i in range (0,len(bitstream_str)):
		bitstream[i] = bitstream_str[i]
	for i in range (0,20):
		for j in range(0,32):
			cfg[i] += (bitstream[i*32+j] << j)
	__abstracted_reg_write(cfg[0], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG0, handle)
	__abstracted_reg_write(cfg[1], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG1, handle)
	__abstracted_reg_write(cfg[2], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG2, handle)
	__abstracted_reg_write(cfg[3], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG3, handle)
	__abstracted_reg_write(cfg[4], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG4, handle)
	__abstracted_reg_write(cfg[5], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG5, handle)
	__abstracted_reg_write(cfg[6], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG6, handle)
	__abstracted_reg_write(cfg[7], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG7, handle)
	__abstracted_reg_write(cfg[8], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG8, handle)
	__abstracted_reg_write(cfg[9], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG9, handle)
	__abstracted_reg_write(cfg[10], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG10, handle)
	__abstracted_reg_write(cfg[11], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG11, handle)
	__abstracted_reg_write(cfg[12], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG12, handle)
	__abstracted_reg_write(cfg[13], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG13, handle)
	__abstracted_reg_write(cfg[14], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG14, handle)
	__abstracted_reg_write(cfg[15], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG15, handle)
	__abstracted_reg_write(cfg[16], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG16, handle)
	__abstracted_reg_write(cfg[17], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG17, handle)
	__abstracted_reg_write(cfg[18], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG18, handle)
	__abstracted_reg_write(cfg[19], Digital_RegisterFile.SCI_REG_PetirocCfg0_REG_CFG19, handle)
	__abstracted_reg_write(0, Digital_RegisterFile.SCI_REG_PetirocCfg0_START_REG_CFG, handle)
	__abstracted_reg_write(1, Digital_RegisterFile.SCI_REG_PetirocCfg0_START_REG_CFG, handle)
	__abstracted_reg_write(0, Digital_RegisterFile.SCI_REG_PetirocCfg0_START_REG_CFG, handle)
