import serial
import time
import struct
import json
import os
import select
import random
import time
import threading

port_serial = "/dev/ttyUSB0"
data_fifo = os.open('/tmp/data_fifo', os.O_RDWR | os.O_NONBLOCK)
control_fifo = os.open('/tmp/control_fifo', os.O_RDWR | os.O_NONBLOCK)
baud = 9600
ser = None
CRLF = '\r\n'
ID_list = {1:9, 2:6}
control_data_list = []
control_data_flag = False


ps_on = struct.pack("7s", bytearray('OUT 1\r\n', 'utf-8'))
ps_off = struct.pack("7s", bytearray('OUT 0\r\n', 'utf-8'))


def SetVoltage(value):
    x = ('PV %2.2f' % value)+CRLF
    y = struct.pack("9s", bytearray(x, 'utf-8'))
    response = WriteToPort(ser, y)
    return response.decode('utf-8')


def SetCurrent(value):
    x = ('PC %2.2f' % value)+CRLF
    y = struct.pack("9s", bytearray(x, 'utf-8'))
    response = WriteToPort(ser, y)
    return response.decode('utf-8')


def WriteToPort(port, value):
    port.write(value)
    ret = port.readline()
    #print(" WriteToPort response----", ret)
    return ret.decode('utf-8')


def SelectADR(ID):
    x = 'ADR ' + '%.1s' % (ID) + CRLF
    y = (bytearray(x, 'utf-8'))
    print(' select id --', y)
    ret = WriteToPort(ser, struct.pack('=7s', y))
    print("return value in write   ", ret)
    return ret


def ReadFromPort(port_serial):
    output = port_serial.read(38)
    return output


def GetAllParams():
    z1 = "DVC?\r\n"
    z = (bytearray(z1, 'utf-8'))
    buf = WriteToPort(ser, struct.pack("=6s", z))
    params = buf.split(',')
    print("parama  ",params)
    return params


def Test(data_list):
    print('in Test ****', data_list)

    ret = SelectADR(ID_list[data_list[0]])
    print('  %%%%%% ret ---', ret)
    if ret == "OK\r":
        #ON Command
        if data_list[3] == 1:
            r1 = WriteToPort(ser, ps_on)
            print('****************************************** ', r1)
            if r1=='OK\r':
                str1 = 'flite -t \'PowerSupply %d ON\' &'%ID_list[data_list[0]]
                print(' ON SUCESS &&& TEST')
                os.system(str1)
            else:
                print('PS ON failed %d '% ID_list[data_list[0]])
        #OFF Command
        else:
            r1 = WriteToPort(ser, ps_off)
            if r1=='OK\r':
                str1 = 'flite -t \'PowerSupply %d OFF\' &' % ID_list[data_list[0]]
                os.system(str1)
            else:
                print('PowerSupply %d OFF Failed ' % ID_list[data_list[0]])
    else:
        print("&&& TEST ******************* NOT OK  ")


def ReadServerEvent():
    global control_data_flag
    while (1):
        read_fd, write_fd, err_fd = select.select([control_fifo], [], [], 10)
        for fd in read_fd:
            data = os.read(fd, 512)
            print("**************  ", data)
            params = json.loads(data.decode('utf-8'))
            print("Data From Server  ", data, data.decode('utf-8'))

            li = []
            li.append(params['id'])
            li.append(params['voltage'])
            li.append(params['current'])
            li.append(params['control'])
            control_data_list.append(li)
            control_data_flag = True

            #print("id %d, voltage %f, current %f, control %d" % (data['id'], data['voltage'], data['current'], data['control']))


def ReadSerialPortData():
    global control_data_flag
    while True:
        #for i in range(int(len(ID_list))):
        for key, val in ID_list.items():
            ret = SelectADR(val)
            if ret == "OK\r":
                time.sleep(.1)
                param = GetAllParams()
                if param != ['']:
                    data = {}
                    data['id'] = key
                    data['voltage'] = param[0]
                    data['current'] = param[2]
                    json_obj = json.dumps(data)
                    os.write(data_fifo, bytearray(json_obj, 'utf-8'))
                    #print('json _obj sent', data)
            else:
                    print(" read error at %d" % val)


            if control_data_flag == True:
                print("$$$$$$$$ Got Control Data $$$$$$$$$$")
                while(len(control_data_list) != 0):
                    data_list = control_data_list.pop()
                    print(data_list)
                    Test(data_list)
                control_data_flag = False
            time.sleep(.1)


if __name__ == "__main__":
    ser = serial.Serial(port_serial, baud, timeout=0.1)
    if ser.isOpen():
        print(ser.name + ' opened...')
    else:
        print(ser.name + ' failed...')

    t2 = threading.Thread(target=ReadSerialPortData, name="Data")
    t2.start()

    ReadServerEvent()

    #t1.join()
    t2.join()

    ser.close()
