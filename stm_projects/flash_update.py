import os
import struct
import serial

MESSAGE_TOKEN            = 0x23
CHANGE_BANK_REQUEST      = 0x43
BOOT_UPDATE_REQUEST      = 0x42
FIRMWARE_VERSION_REQUEST = 0x41

BOOT_ACK                 = 0x5f
BOOT_NACK                = 0xaa


def compute_crc(buff, length):
    crc = 0xFFFFFFFF
    #print(length)
    for byte in buff[0:length]:
        crc = crc ^ (byte)
        for i in range(32):
            if(crc & 0x80000000):
                crc = (crc << 1) ^ 0x04C11DB7
            else:
                crc = (crc << 1)
    
    return crc &  0xFFFFFFFF

def update_flash_mem(serial_com, file_name):
        WINDOW_SIZE  = 128
        try:
            flash_bin_file = open(file_name, 'rb')
        except:
            Exception('cannot open the bin file')
        size = os.path.getsize(file_name)
        # data token and command
        data_token = [MESSAGE_TOKEN, BOOT_UPDATE_REQUEST]
        data_token_bytes = bytes()
        data_token_bytes = data_token_bytes.join((struct.pack('<'+format, val) for format,val in zip('BB',data_token)))
        size_copy = size
        while size > 0:
            # actual data
            data_sent = flash_bin_file.read(WINDOW_SIZE)
            size = size - len(data_sent)
            data_sent = data_token_bytes + struct.pack('<H',len(data_sent)) + data_sent
            send_data_serial(serial_com, data_sent)
            print('Firmware update ' + str(int(100 * (size_copy - size)/size_copy)) +' %' +': ' + int(50 * (size_copy - size)/size_copy) * '#', end = '\r')
            if read_boot_reply(serial_com) != BOOT_ACK:
                print("flash update failed ")
                Exception("flash update failed")
                break

        if size == 0:
            print('Firmware update ' + str(int(100 * (size_copy - size)/size_copy)) +' %' +': ' + \
                int(20 * (size_copy - size)/size_copy) * '#')
            print('Firmware update is over')
            


def read_boot_reply(serial_com):
    ack_value = serial_com.read(1)
    if len(ack_value) > 0 and ack_value[0] == BOOT_ACK:
        return BOOT_ACK
    else:
        return BOOT_NACK
    
def send_data_serial(serial_com, data):
    data =  data + (struct.pack('<I',compute_crc(data, len(data))))
    serial_com.write(data)

def read_firmware_version(serial_com):
    command_message = [MESSAGE_TOKEN, FIRMWARE_VERSION_REQUEST, 0]
    b = bytes()
    b = b.join((struct.pack('<'+format, val) for format,val in zip('BBH',command_message)))
    send_data_serial(serial_com, b)

    raw_data = serial_com.read(27)
    message = struct.unpack("%ds" % len(raw_data), raw_data)
    message = message[0].decode("utf-8")
    print(message)

def change_firmware(serial_com):
    command_message = [MESSAGE_TOKEN, CHANGE_BANK_REQUEST, 0]
    b = bytes()
    b = b.join((struct.pack('<'+format, val) for format,val in zip('BBH',command_message)))
    send_data_serial(serial_com, b)
    if read_boot_reply(serial_com) != BOOT_ACK:
        Exception("flash change failed")
            

######################################################################################################
comport = "COM3"
serial_com = serial.Serial(port = comport,baudrate = 115200, timeout = 15)

message = "Ukulele ukulele \n \0"

message = bytes(message, 'utf-8')
while(True):
    command = int(input("enter the command number (1 - update, 2 - change, 3 - check): "))
    if command == 1:
        update_flash_mem(serial_com, "steppe_school_custom_bootloader_l432kc_application.bin")
    elif command == 2:
        change_firmware(serial_com)
    elif command == 3:
        read_firmware_version(serial_com)
    else:
        break