from animatics_motor_interface import AnimaticsProgram
import time

def test():
    print(f"Motor Test start: {time.time()}")
    file_name = "pythonCreated.sms"
    program = AnimaticsProgram(file_name=file_name)

    # create and write program
    program.createProgram()

    program.resetErrorFlag()
    program.setAcceleration(100)
    program.setVelocity(1000000)
    program.setPosition(100000)
    program.writeGo()
    program.writeTWAIT()
    program.setPosition(0)
    program.writeGo()

    # upload the program
    program.uploadProgram()

    print(f"Motor Test end: {time.time()}")


if __name__ == "__main__":
    test()