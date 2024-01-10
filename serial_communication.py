"""
serial_communication.py: This script attempts to use serial communication to send commands to the Animatics SM2340D 415C motor
"""
import serial
from binascii import hexlify
import time

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

# open a program designed to spin the motor
temp = ""
with open("../Animatics Motors SMX Files/SMI1.sms", "r") as inFile:
    for line in inFile:
        temp += line
    inFile.close()

temp_in_ascii = temp.encode('ascii')
temp_in_hex = temp_in_ascii.hex()


# the above program in hex should be
hex_string = "52 55 4E 3F 0A 5A 53 0A 41 3D 31 30 30 0A 56 3D 31 30 30 30 30 30 30 0A 50 3D 31 30 30 30 30 30 0A 47 0A 54 57 41 49 54 0A 50 3D 30 0A 47 0A 50 52 49 4E 54 28 22 50 72 6F 67 72 61 6D 20 46 69 6E 69 73 68 65 64 20 3A 44 22 2C 23 31 33 29 0A 45 4E 44 0A"

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
        time.sleep(1)
        read_bytes = ser.read_all()
        print(read_bytes.decode('utf-8'))
    ser.close()
