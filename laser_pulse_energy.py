'''
laser_pulse_energy.py: This script's purpose is to understand how to interface with the Molectron EPM 2000 over serial
                       using SCPI commands.
'''

import serial
import time

__authors__ = ["Spencer Pollard", "Emilio A Choncha Alarcon"]
__credits__ = ["Spencer Pollard", "Emilio A Choncha Alarcon", "Shane Mayor"]

class Molectron:
    def __init__(self, port, baud, parity, stop_bit, timeout):
        self.port = port
        self.baud = baud
        self.parity = parity
        self.stop_bit = stop_bit
        self.timeout = timeout

    def __write(self, command, show_error=False):
        ser = serial.Serial(port=self.port, baudrate=self.baud, parity=self.parity, stopbits=self.stop_bit, timeout=self.timeout)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(f'{command}\r'.encode('ascii'))
        s = ser.readline().decode('utf-8')
        if show_error:
            print(s)
    
        ser.close()

    # Getter functions
    def get_port(self):
        return self.port
    
    def get_baud(self):
        return self.baud
    
    def get_parity(self):
        return self.parity

    def get_stop_bit(self):
        return self.stop_bit
    
    def get_timeout(self):
        return self.timeout

    # SCPI Commands
    def printIDN(self):
        command = "*IDN?"
        self.__write(command,True)
        
    def enableBacklight(self, show_error=False):
        command = "syst opt bac on"
        self.__write(command, show_error)

    def disableBacklight(self, show_error=False):
        command = "syst opt bac off"
        self.__write(command, show_error)

    def writeCommand(self, command, show_error=False):
        self.__write(command, show_error)

    def readBuffer(self, show_error=False):
        ser = serial.Serial(port=self.port, baudrate=self.baud, parity=self.parity, stopbits=self.stop_bit, timeout=self.timeout)
        s = ser.read_all().decode('utf-8')
        if show_error:
            print(s)
        ser.close()


if __name__ == "__main__":
    temp = []
    port = 'COM1'
    baud = 38400
    parity = 'N'
    stopbits = 1
    timeout = 2
    meter = Molectron(port, baud, parity, stopbits, timeout)
    meter.writeCommand("out cont on")

    ser = serial.Serial(port=port, baudrate=baud, parity=parity, stopbits=stopbits, timeout=timeout)

    start_time = time.time()
    curr_time = time.time()
    while curr_time - start_time < 4.95:
        print(f"diff: {curr_time - start_time}")
        s = ser.readline().decode('utf-8').strip()
        print(f"s: {s}")
        temp.append(s)
        curr_time = time.time()

    ser.close()

    meter.writeCommand("out cont off")



    print(f"temp: {temp}")
    print(f'length of temp: {len(temp)}')