"""
terminal_block.py: This script is attempting to interface the NI DAQ PCIe-6323 Multifunction I/O card with the NI SCC-68
"""

import nidaqmx as ni
import numpy as np
import time
from multiprocessing import Process, Queue
import serial
import matplotlib.pyplot as plt

__authors__ = ["Spencer Pollard", "Emilio A Choncha Alarcon"]
__credits__ = ["Spencer Pollard", "Emilio A Choncha Alarcon", "Shane Mayor"]

def quadrature_encoder(queue):
    print(f"Quadrature encoder start: {time.time()}")
    x = []
    y = []

    with ni.Task() as task:
        # To use ctr0, the two encoder channels are plugged into PFI 8 and PFI 10 (37 and 45 on SCC-68)
        task.ci_channels.add_ci_ang_encoder_chan(counter="/Dev2/ctr0", 
                                                 name_to_assign_to_channel="encoder", 
                                                 decoding_type=ni.constants.EncoderType.X_1, # originally was X_1
                                                 zidx_enable=False, 
                                                 pulses_per_rev=1000,
                                                 units=ni.constants.AngleUnits.DEGREES,
                                                 initial_angle=0)

        # Start task
        task.control(ni.constants.TaskMode.TASK_START)

        time.sleep(4)

        start_motor()

        t_end = time.time() + 4
        while time.time() < t_end:
            # Read both encoders and monitor the position
            position = task.read()
            print(position)
            # print(f"A: {encoderA_position}")

            # Append the data to the lists
            x.append(time.time())
            y.append(position)

        stop_motor()

        # Stop task
        task.control(ni.constants.TaskMode.TASK_STOP)

    queue.put((x, y))
    print(f"Quadrature encoder end: {time.time()}")
    

def start_motor():
    file_data = 'RUN\n'
    sub_packet = bytearray(b'')

    for i in range(len(file_data)):
        sub_packet.append(bytes(file_data, 'ascii')[i])
        
    with serial.Serial('COM10', 9600, timeout=2) as ser:
        ser.write(sub_packet)
        ser.read(8)

def stop_motor():
    file_data = 'END\n'
    sub_packet = bytearray(b'')

    for i in range(len(file_data)):
        sub_packet.append(bytes(file_data, 'ascii')[i])
        
    with serial.Serial('COM10', 9600, timeout=2) as ser:
        ser.write(sub_packet)
        ser.read(8)

if __name__ == "__main__":
    # Create a queue
    q = Queue()
    encoder = Process(target=quadrature_encoder, args=(q,))
    encoder.start()
    x, y = q.get()

    print(f"max: {np.max(y)}")
    print(f"min: {np.min(y)}")

    plt.plot(x,y)

    plt.show()
