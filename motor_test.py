"""
terminal_block.py: This script is attempting to interface the NI DAQ PCIe-6323 Multifunction I/O card with the NI SCC-68
"""

import nidaqmx as ni
import time
from multiprocessing import Process, Queue
import serial
import matplotlib.pyplot as plt

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

def edge_counting_encoderA(queue):
    print(f"Edge counting A start: {time.time()}")
    x = []
    y = []

    with ni.Task() as task:
        # create counter input task to count rising edges (default setting) on the Dev2/ctr0 channel
        task.ci_channels.add_ci_count_edges_chan(counter="/Dev2/ctr0", name_to_assign_to_channel="countEdges") # PFI8 => pin 37
        
        result = 0

        start_motor()

        # start task
        task.control(ni.constants.TaskMode.TASK_START)

        t_end = time.time() + 5
        while time.time() < t_end:
            result = task.read(number_of_samples_per_channel=ni.constants.READ_ALL_AVAILABLE, timeout=120)[-1]
            x.append(time.time())
            y.append(result)

        # end task
        task.control(ni.constants.TaskMode.TASK_STOP)

    stop_motor()

    queue.put((x,y))
    print(f"Edge counting A end: {time.time()}")

def edge_counting_encoderB(queue):
    print(f"Edge counting B start: {time.time()}")
    with ni.Task() as task:
        # create counter input task to count rising edges (default setting) on the Dev2/ctr0 channel
        task.ci_channels.add_ci_count_edges_chan(counter="/Dev2/ctr1", name_to_assign_to_channel="countEdges") # PFI3 => pin 42

        result = 0

        # start task
        task.control(ni.constants.TaskMode.TASK_START)

        t_end = time.time() + 5
        while time.time() < t_end:
            result = task.read(number_of_samples_per_channel=ni.constants.READ_ALL_AVAILABLE, timeout=120)[-1]

        # end task
        task.control(ni.constants.TaskMode.TASK_STOP)
        
        print(f"Edge counting B end: {time.time()}")
        queue.put(result)

        return result

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

    encoderA = Process(target=edge_counting_encoderA, args=(q,))
    # encoderB = Process(target=edge_counting_encoderB, args=(q,))

    encoderA.start()
    # encoderB.start()

    x, y = q.get()

    plt.plot(x,y)
    plt.show()
