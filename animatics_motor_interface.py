"""
animatics_motor_interface.py: This program is suppose to help build the scripts to properly control the Animatics SM2340D 415C motor 
"""

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

import os

'''
how I think I should make python interface with the motor

init command to create a temporary script file that will be used to program the motor
commands that open this temporary file to write appropriate commands to it
'''

# class to house the program that is to be uploaded to the motor
class AnimaticsProgram:
    # constructors
    def __init__(self, file_path=None, file_name=None):
        self.file_data = ""
        self.file_path = "./temp"
        self.file_name = "temp"
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

    # other methods
    def uploadProgram(self,):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write(f"END\n")
                # do the serial writing stuff
                programFile.close()
            self.file_data += "END\n"
        except:
            print("[uploadProgram ERROR]: Failed to open temp file")

    def writePRINT(self, passed_string):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write(f"PRINT({passed_string})\n")
                programFile.close()
            self.file_data += f"PRINT({passed_string})\n"
        except:
            print("[writePRINT ERROR]: Failed to open temp file")

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

    def writeTWAIT(self):
        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write("TWAIT\n")
                programFile.close()
            self.file_data += "TWAIT\n"
        except:
            print("[writeTWAIT ERROR]: Failed to open temp file")


if __name__ == "__main__":
    program = AnimaticsProgram(file_name="pythonCreated.sms")

    program.createProgram()
    program.resetErrorFlag()
    program.setAcceleration(100)
    program.setVelocity(1000000)
    program.setPosition(100000)
    program.writeGo()
    program.writeTWAIT()
    program.setPosition(0)
    program.writeGo()
    program.writePRINT('"Program Finished :D",#13')
    program.uploadProgram()

    print(program.getFileData())