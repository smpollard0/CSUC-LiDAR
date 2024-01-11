"""
serial_communication.py: This script attempts to use serial communication to send commands to the Animatics SM2340D 415C motor
"""
import serial
from binascii import hexlify
import time

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

def serial_write(file_path):
    print(time.time())
    # open a program designed to spin the motor
    temp = ""
    try:
        with open(file_path, "r") as inFile:
            for line in inFile:
                temp += line
            inFile.close()
    except:
        raise Exception("Invalid file path")

    temp_in_ascii = temp.encode('ascii')

    # mostly works? currently I believe there is a timing issue where I'm sending bytes before I receieve confirmation of the ones I just sent
    with serial.Serial('COM1', 9600) as ser:
        remaining_chars = len(bytes(temp, 'ascii'))
        # try to send every 8 bytes
        for i in range(0, len(bytes(temp, 'ascii')), 8):
            # if there 8 or more bytes available, write those
            if remaining_chars > 8:
                # create byte array of the next 8 bytes and send those
                sub_packet = bytearray(b'')
                for j in range(8):
                    sub_packet.append(bytes(temp, 'ascii')[i+j])
                remaining_chars -= 8
                
            else:
                sub_packet = bytearray(b'')
                for k in range(remaining_chars):
                    sub_packet.append(bytes(temp, 'ascii')[i+k])
                remaining_chars -= remaining_chars
            
            ser.write(sub_packet)
            time.sleep(0.5) # this is a weird work around to my current issue
            read_bytes = ser.read_all()
            print(read_bytes.decode('utf-8'))
        ser.close()