"""
signal_conditioning_box.py: This script is attempting to interface the NI DAQ PCIe-6323 Multifunction I/O card with the NI SCC-68
"""

import nidaqmx as ni

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

# keep in mind pylablib for interfacing using the COM serial ports

# figure out how to use the scc-ft01 cards on the scc-68 with the pcie-6323
with ni.Task() as task:
    print("pain")