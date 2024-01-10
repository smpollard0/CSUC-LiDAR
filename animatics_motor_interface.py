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
        self.file_data = "RUN\n"
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

        try:
            with open(f"{self.file_path}/{self.file_name}", "a") as programFile:
                programFile.write("RUN\n")
        except:
            print("[createProgram ERROR]: Failed to create temp file")


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

        return -1


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


if __name__ == "__main__":
    program = AnimaticsProgram(file_name="SM1")

    program.createProgram()
    program.setVelocity(100)
    program.uploadProgram()
    