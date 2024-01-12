"""
capture_waveforms.py: This script is responsible for collecting waveform data using the NI DAQ PCI-5122 Oscilloscope Card.
"""
import nidaqmx as ni
import time
import multiprocessing

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

def collect_waveform_data(num_of_samples, passed_sample_rate, queue):
    print(f"Collect waveform start: {time.time()}")
    # create variables for number of samples and desired sample rate
    sample = num_of_samples
    sample_rate = passed_sample_rate
    data = []

    # create an NI task
    with ni.Task() as task:
        # create an analog input voltage channel which has device name Dev where /0 indicates the specific channel on the card
        task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/0")
        
        # configure the card's timing to allow for continous data collection 
        task.timing.cfg_samp_clk_timing(rate=sample_rate, sample_mode=ni.constants.AcquisitionType.CONTINUOUS, samps_per_chan=sample)

        # read in the data
        temp = task.read(number_of_samples_per_channel=sample)
        # place all data from temp into data array
        for i in temp:
            data.append(i)

    x = list(range(len(data)))

    queue.put(x)
    queue.put(data)

    print(f"Collect waveform end: {time.time()}")
    return x, data

