import niscope
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    voltage_array = np.array([])

    # Create a session for the device
    with niscope.Session('Dev1') as session:
        # Configure vertical settings for channel 0
        session.channels['1'].configure_vertical(
            range=5.0,  # Vertical range in volts
            coupling=niscope.VerticalCoupling.DC
        )

        # Configure horizontal timing
        session.configure_horizontal_timing(
            # if the min sample rate >= min num pts you get discontinuities
            min_sample_rate=1_000_000,  # 1 MS/s
            min_num_pts=500_000,           # Number of points per record
            ref_position=50.0,          # Position of the trigger in percentage
            num_records=1,              # Number of records
            enforce_realtime=True
        )

        # Configure edge trigger with external source
        session.configure_trigger_edge(
            trigger_source='VAL_EXTERNAL',       # External trigger source
            trigger_coupling=niscope.TriggerCoupling.DC,
            level=1.0,                           # Trigger level in volts
            slope=niscope.TriggerSlope.POSITIVE  # Trigger on rising edge
        )

        # Initiate acquisition
        with session.initiate():
            # Fetch data from channel 0
            try:
                print('Waiting for trigger...')
                waveforms = session.channels['1'].fetch(num_records=1,timeout=-1)
                voltage_data = waveforms[0].samples  # Extract voltage data
                voltage_array = np.array(voltage_data)
                print('Trigger found!')
            except:
                print("No data collected")

        

    x = np.arange(len(voltage_array))
    plt.plot(x,voltage_array)
    plt.show()
    