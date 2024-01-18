"""
capture_waveforms.py: This script is responsible for collecting waveform data using the NI DAQ PCI-5122 Oscilloscope Card.
"""
import nidaqmx as ni
from LedIndicatorWidget import *
from datetime import datetime

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

def collect_waveform_data(num_of_samples, passed_sample_rate, LED, bool_to_write, file_location):
    if bool_to_write:
        # create variables for number of samples and desired sample rate
        sample = num_of_samples
        sample_rate = passed_sample_rate
        data = []

        # create an NI task
        with ni.Task() as task:
            LED.setChecked(True)
            # create an analog input voltage channel which has device name Dev where /1 indicates the specific channel on the card
            task.ai_channels.add_ai_voltage_chan(physical_channel="Dev1/1")
            
            # configure the card's timing to allow for continous data collection 
            task.timing.cfg_samp_clk_timing(rate=sample_rate, sample_mode=ni.constants.AcquisitionType.CONTINUOUS, samps_per_chan=sample)

            # read in the data
            temp = task.read(number_of_samples_per_channel=sample)
            # place all data from temp into data array
            for i in temp:
                data.append(i)

        x = list(range(len(data)))
        now = datetime.now()
    
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

        # write all this data to file specified by passed parameter
        with open(f"{file_location}/{dt_string}", "w") as outFile:
            for i in range(len(x)):
                outFile.write(f"{x[i]},{data[i]}\n")
            outFile.close()

        # turn off the led
        LED.isChecked(False)