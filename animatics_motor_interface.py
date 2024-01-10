"""
animatics_motor_interface.py: this program is suppose to help build the scripts to properly control the Animatics SM2340D 415C motor 
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
class AnimaticsProgram():
    # constructors
    def __init__(self):
        self.file_data = ""
        self.file_path = ""
        self.file_name = ""
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
    def __init__(self, file_name):
        self.file_name = file_name

    # setters
        
    # getters

# 
def createProgram(file_name):

    try:
        os.makedirs("./temp")
    except:
        pass
    
    file = open(f"./temp/{file_name}.sms", "a")

    return file

# 
def setVelocity(passed_velocity):

    return -1

# 
def setAcceleration(passed_acceleration):

    return -1

#
def uploadProgram():

    return -1

if __name__ == "__main__":
    program = createProgram("bob's burgers")