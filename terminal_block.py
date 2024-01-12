"""
terminal_block.py: This script is attempting to interface the NI DAQ PCIe-6323 Multifunction I/O card with the NI SCC-68
"""

import nidaqmx as ni
import time

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

# figure out how to use the scc-ft01 cards on the scc-68 with the pcie-6323

def edge_counting():
    print(f"Edge counting start: {time.time()}")
    with ni.Task() as task:
        # create counter input task to count rising edges (default setting) on the Dev2/ctr0 channel
        task.ci_channels.add_ci_count_edges_chan(counter="/Dev2/ctr0", name_to_assign_to_channel="countEdges")

        result = 0

        # start task
        task.control(ni.constants.TaskMode.TASK_START)

        t_end = time.time() + 15
        while time.time() < t_end:
            result = task.read(number_of_samples_per_channel=ni.constants.READ_ALL_AVAILABLE, timeout=120)[-1]

        # end task
        task.control(ni.constants.TaskMode.TASK_STOP)
        
        print(f"Final Count: {result}")
        print(f"Edge counting end: {time.time()}")

if __name__ == "__main__":
    edge_counting()
        