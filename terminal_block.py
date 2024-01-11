"""
terminal_block.py: This script is attempting to interface the NI DAQ PCIe-6323 Multifunction I/O card with the NI SCC-68
"""

import nidaqmx as ni

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

# keep in mind pylablib for interfacing using the COM serial ports

# figure out how to use the scc-ft01 cards on the scc-68 with the pcie-6323
# 

def edgeCounting(num_of_samples, passed_sample_rate):
    sample = num_of_samples
    sample_rate = passed_sample_rate

    count = 0

    with ni.Task() as task:
        # create counter input task to count rising edges (default setting) on the Dev2/ctr0 channel
        task.ci_channels.add_ci_count_edges_chan(counter="Dev2/ctr0")
        
        # configure the card's timing to allow for continous data collection 
        task.timing.cfg_samp_clk_timing(rate=sample_rate, sample_mode=ni.constants.AcquisitionType.CONTINUOUS, samps_per_chan=sample)
        temp = task.read(number_of_samples_per_channel=sample)

        # place all data from temp into data array
        

if __name__ == "__main__":
    edgeCounting(10000,100000000)
        