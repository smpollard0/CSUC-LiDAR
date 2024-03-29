"""
animatics_motor_interface.py: This program is suppose to help build the scripts to properly control the Animatics SM2340D 415C motor 
"""

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

import os
import time
import serial

'''
how I think I should make python interface with the motor

init command to create a temporary script file that will be used to log the program to the motor
commands that open this temporary file to write appropriate commands to it
'''

# class to house the program that is to be uploaded to the motor
class AnimaticsProgram:
    # constructors
    def __init__(self, file_path=None, file_name=None):
        self.file_data = ""
        self.file_path = "./temp"
        self.file_name = "temp"
        self.isRunning = False
        if file_path == None:
            if file_name != None:
                self.file_name = file_name
        elif file_name == None:
            if file_path != None:
                self.file_path = file_path
        else:
            self.file_name = file_name
            self.file_path = file_path   

    # program creation
    def createProgram(self):
        if not os.path.exists(self.file_path):
            try:
                os.makedirs(self.file_path)
            except:
                print("[createProgram ERROR]: Invalid file path or file path already exists")
        if os.path.isfile(f"{self.file_path}/{self.file_name}"):
            os.remove(f"{self.file_path}/{self.file_name}")

    # setters
    def setFileName(self, file_name):
        self.file_name = file_name

    def setFilePath(self, file_path):
        self.file_path = file_path

    def setVelocity(self, passed_velocity):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write(f"V={passed_velocity}\n")
                programFile.close()
            self.file_data += f"V={passed_velocity}\n"
        except:
            print("[setVelocity ERROR]: Failed to open temp file")

    def setAcceleration(self, passed_acceleration):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write(f"A={passed_acceleration}\n")
                programFile.close()
            self.file_data += f"A={passed_acceleration}\n"
        except:
            print("[setAcceleration ERROR]: Failed to open temp file")

    def setPosition(self, passed_position):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write(f"P={passed_position}\n")
                programFile.close()
            self.file_data += f"P={passed_position}\n"
        except:
            print("[setAcceleration ERROR]: Failed to open temp file")


    # getters
    def getFileData(self):
        return self.file_data
    
    def getFilePath(self):
        return self.file_path

    # other methods
    # some other logic needs to be here, I need to either figure out the timing with sending and receiving data, or physically calculate how long each command takes to run before trying to send another one
    def __serial_write(self):
        # mostly works?
        # CURRENT ISSUE: there's some issue with writing the bytes too quickly which is why there's a time.sleep()
        with serial.Serial('COM1', 9600, timeout=2) as ser:
            remaining_chars = len(bytes(self.file_data, 'ascii'))
            # send every 8 bytes
            for i in range(0, len(bytes(self.file_data, 'ascii')), 8):
                # create byte array of the next 8 bytes and send those
                sub_packet = bytearray(b'')
                # if there 8 or more bytes available, write those
                if remaining_chars > 8:
                    for j in range(8):
                        sub_packet.append(bytes(self.file_data, 'ascii')[i+j])
                    remaining_chars -= 8
                    
                else:
                    for k in range(remaining_chars):
                        sub_packet.append(bytes(self.file_data, 'ascii')[i+k])
                    remaining_chars -= remaining_chars
                
                ser.write(sub_packet)
                time.sleep(1) # weird workaround for timing issue
                ser.read(8)

            ser.close()


    def uploadProgram(self):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write(f"END\n")
                programFile.close()
            self.__serial_write()
            self.file_data += "END\n"
            self.isRunning = True
        except:
            print("[uploadProgram ERROR]: Failed to open temp file or write over serial")

    def writePRINT(self, passed_string):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write(f"PRINT({passed_string})\n")
                programFile.close()
            self.file_data += f"PRINT({passed_string})\n"
        except:
            print("[writePRINT ERROR]: Failed to open temp file or port is already being used")

    def resetErrorFlag(self):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write("ZS\n")
                programFile.close()
            self.file_data += "ZS\n"
        except:
            print("[resetErrorFlag ERROR]: Failed to open temp file")
    
    def writeGo(self):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write("G\n")
                programFile.close()
            self.file_data += "G\n"
        except:
            print("[writeGo ERROR]: Failed to open temp file")

    # i think there needs to be more done here...
    def writeTWAIT(self):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write("TWAIT\n")
                programFile.close()
            self.file_data += "TWAIT\n"
        except:
            print("[writeTWAIT ERROR]: Failed to open temp file")