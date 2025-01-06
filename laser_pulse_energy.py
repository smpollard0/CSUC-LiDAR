'''

'''

import serial

if __name__ == "__main__":
    command = '*IDN?\r\n'
    packet = bytearray(b'')

    for i in range(len(command)):
        packet.append(bytes(command, 'ascii')[i])
        
    with serial.Serial('COM6', 4800, timeout=1) as ser:
        ser.write(packet)
        s = ser.read_until('\r\n')
        print(s)
