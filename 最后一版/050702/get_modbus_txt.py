#!/usr/bin/env python
#_*_coding:utf-8_*_
#@Time :2019年5月7日 0007下午 03:32:54
#@Author:zwl
#@File:get_modbus_txt.py
#@Software:PyCharm
import time
import datetime
import serial
import serial.tools.list_ports
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import binascii
from binascii import *
from crcmod import *
import threading
import multiprocessing
import queue

def crc16Add(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    readcrcout = hex(crc16(unhexlify(read))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = "".join(str_list)
    # print(crc_data)
    read = read.strip() + crc_data[4:] + crc_data[2:4]
    # print('CRC16校验:', crc_data[4:] + ' ' + crc_data[2:4])
    # print('增加Modbus CRC16校验：>>>', read)
    return read

PORT = 'COM5'  # windows
PORT = '/dev/ttyUSB0' #linux接口 

def HexToByte( hexStr ):
    return bytes.fromhex(hexStr)
def str_to_hex(s):
    return ''.join([hex(ord(c)).replace('0x', '') for c in s])
def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])
def str_to_bin(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])
def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])
def modbus_getdate(slave_id ,start_addr,date_len):
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT,
                                                    baudrate=19200,
                                                    bytesize=8,
                                                    parity='O',
                                                    stopbits=1,
                                                    xonxoff=0))
        # logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
        master.set_timeout(5)
        master.set_verbose(True)

        # print('connected')
        # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 125))
        # read 方法
        holding_date = master.execute(slave_id, cst.READ_HOLDING_REGISTERS, start_addr, date_len)
        holding_data125 = []
        for i in range(len(holding_date)) :
            holding_data125.append('%04x'%(holding_date)[i])  # append()在Tmp1列表末尾添加新的对象
        all_holding_data = '%02x'%slave_id + '03fa' + ''.join(holding_data125)
        # print(all_holding_data)
        all_holding_data_crc16Add = crc16Add(all_holding_data)# 增加Modbus CRC16校验值后的值
        # print(all_holding_data_crc16Add)
        return str(all_holding_data_crc16Add)
        # write方法
        # print(master.execute(35, cst.WRITE_MULTIPLE_REGISTERS, 9, output_value=[1]))
    except modbus_tk.modbus_rtu.ModbusInvalidResponseError as err:
        print(err)
t1 = time.clock()
s1=modbus_getdate(slave_id=1,start_addr=0,date_len=125)
t2 =time.clock()
time.sleep(0.1)
s2=modbus_getdate(slave_id=2,start_addr=0,date_len=125)
print(s1)
print(s2)
# print(t2-t1)
# qu = queue.Queue(maxsize=20)
# modbus_s1 = ''
# modbus_s2 = ''
# def f1(s):
#     global modbus_s1
#     global modbus_s2
#     while True:
#         time.sleep(10)
#         print(modbus_s1)
# def m_datas(s):
#     global modbus_s1
#     global modbus_s2
#     while True:
#
#         modbus_s1 = modbus_getdate(slave_id=1, start_addr=0, date_len=125)
#         modbus_s2 = modbus_getdate(slave_id=2, start_addr=0, date_len=125)
#         time.sleep(5)
#
# p1 = threading.Thread(target=m_datas,args=(1,)).start()
# time.sleep(5)
# p2 = threading.Thread(target=f1,args=(1,)).start()
