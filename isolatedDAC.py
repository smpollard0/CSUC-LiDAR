"""
isolatedDAC.py: This program is meant to replace the old DAC.py file as a more isolated program. This program will be strictly displaying and 
monitoring the data acquisition processes and NOT focusing on displaying data.
"""

from laser_pulse_energy import Molectron

from PyQt5.QtWidgets import QApplication
from LedIndicatorWidget import *
import nidaqmx as ni
import niscope
import time
import numpy as np
import serial

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)

def change_led(LED):
    LED.setChecked(not LED.isChecked())

def trigger_helper(LED):
        # this just runs in the background while the program is running
        while True:
            # Create a session for the device
            with niscope.Session('Dev1') as session:
                # Configure vertical settings for channel 0
                session.channels['1'].configure_vertical(
                    range=5.0,  # Vertical range in volts
                    coupling=niscope.VerticalCoupling.DC
                )

                # Configure horizontal timing
                session.configure_horizontal_timing(
                    # If the min sample rate >= min num pts you get discontinuities
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
                    print('Waiting for trigger...')
                    waveforms = session.channels['1'].fetch(num_records=1,timeout=-1)
                    voltage_data = np.array(waveforms[0].samples)  # Extract voltage data
                    print(voltage_data)
                    LED.setChecked(True)
                    time.sleep(0.05)
                    LED.setChecked(False)
            
def update_trigger_led(LED):
    p1 = ProcessRunnable(target=trigger_helper, args=(LED,))
    p1.start()

def pulse_helper(meter):
    meter.writeCommand("out cont on")
    ser = serial.Serial(port=meter.get_port(), 
                        baudrate=meter.get_baud(), 
                        parity=meter.get_parity(), 
                        stopbits=meter.get_stop_bit(), 
                        timeout=meter.get_timeout())
    
    while True:
        s = ser.readline().decode('utf-8').strip()
        print(s)

    ser.close()

def update_pulse_energy(meter):
    p2 = ProcessRunnable(target=pulse_helper, args=(meter,))
    p2.start()

class MainWindow(QMainWindow):
    def set_directory(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.exec()

        self.write_directory = file_dialog.selectedFiles()[0]
        print(self.write_directory)

    def __init__(self):
        super().__init__()
        
        # Variables to be declared at start up
        port = 'COM1'
        baud = 38400
        parity = 'N'
        stopbits = 1
        timeout = 2
        meter = Molectron(port, baud, parity, stopbits, timeout)

        # Need some variable to track if the program is collecting data (also can be used to know when flyback is happening)

        # main window settings
        self.setWindowTitle("LiDAR Data Acquisition Software")
        self.write_directory = "./"

        # menu bar configuration
        menu_bar = self.menuBar()
        file = menu_bar.addMenu('File')
        help = menu_bar.addMenu('Help')

        # create action for help for whatever may go in that menu
    
        file.addAction("Change Write to Disk Location")
        file.triggered.connect(self.set_directory)

        # main groupbox for the window
        # overall group for different data acquisition processes
        group1 = QGroupBox("Status of Data Acquisition Processes")
        vbox1 = QVBoxLayout()
        group1.setLayout(vbox1)

        # status light flashing
        vbox10 = QHBoxLayout()
        group10 = QGroupBox()
        group10.setLayout(vbox10)

        trigger_pulse = QLabel("Trigger Pulse")
        LED9 = LedIndicator()
        LED9.setDisabled(True)
        LED9.on_color_1 = QColor(255,0,0)
        LED9.on_color_2 = QColor(255,0,0)
        LED9.off_color_1 = QColor(0,0,0)
        LED9.off_color_2 = QColor(0,0,0)
        vbox10.addWidget(trigger_pulse)
        vbox10.addWidget(LED9)
        update_trigger_led(LED9)

        # waveform group
        vbox2 = QHBoxLayout()
        group2 = QGroupBox()
        group2.setLayout(vbox2)

        waveform = QLabel("Capture Waveforms")
        LED1 = LedIndicator()
        LED1.setDisabled(True)
        vbox2.addWidget(waveform)
        vbox2.addWidget(LED1)
        
        # get az/al angles group
        vbox3 = QHBoxLayout()
        group3 = QGroupBox()
        group3.setLayout(vbox3)

        azal_angles = QLabel("Get Azimuth and Elevation Angles")
        LED2 = LedIndicator()
        LED2.setDisabled(True)
        vbox3.addWidget(azal_angles)
        vbox3.addWidget(LED2)

        # add display boxes for azimuth and elevation angles
        az_label = QLabel()
        el_label = QLabel()
        az_label.setText("0")
        el_label.setText("0")
        az_label.setAlignment(Qt.AlignCenter)
        el_label.setAlignment(Qt.AlignCenter)
        az_label.setFrameStyle(QFrame.Panel)
        el_label.setFrameStyle(QFrame.Panel)
        az_label.setLineWidth(2)
        el_label.setLineWidth(2)
        vbox3.addWidget(az_label)
        vbox3.addWidget(el_label)

        # get pulse energy group
        vbox4 = QHBoxLayout()
        group4 = QGroupBox()
        group4.setLayout(vbox4)

        pulse_energy = QLabel("Get Pulse Energy")
        LED3 = LedIndicator()
        LED3.setDisabled(True)
        vbox4.addWidget(pulse_energy)
        vbox4.addWidget(LED3)
        update_pulse_energy(meter)

        # add display box for pulse energy
        # edit later to account for 2 pulse energies
        pulse_label = QLabel()
        pulse_label.setText("0")
        pulse_label.setText("0")
        pulse_label.setAlignment(Qt.AlignCenter)
        pulse_label.setFrameStyle(QFrame.Panel)
        pulse_label.setLineWidth(2)
        vbox4.addWidget(pulse_label)
        
        # get date/time group
        vbox5 = QHBoxLayout()
        group5 = QGroupBox()
        group5.setLayout(vbox5)

        date_time = QLabel("Get Date and Time")
        LED4 = LedIndicator()
        LED4.setDisabled(True)
        vbox5.addWidget(date_time)
        vbox5.addWidget(LED4)

        # add display boxes for date and time
        date_label = QLabel()
        time_label = QLabel()
        date_label.setText("0")
        time_label.setText("0")
        date_label.setAlignment(Qt.AlignCenter)
        time_label.setAlignment(Qt.AlignCenter)
        date_label.setFrameStyle(QFrame.Panel)
        time_label.setFrameStyle(QFrame.Panel)
        date_label.setLineWidth(2)
        time_label.setLineWidth(2)
        vbox5.addWidget(date_label)
        vbox5.addWidget(time_label)

        # get Pitch and Roll group
        vbox6 = QHBoxLayout()
        group6 = QGroupBox()
        group6.setLayout(vbox6)

        pitch_roll = QLabel("Get Pitch and Roll")
        LED5 = LedIndicator()
        LED5.setDisabled(True)
        vbox6.addWidget(pitch_roll)
        vbox6.addWidget(LED5)

        # add display boxes for pitch and roll
        pitch_label = QLabel()
        roll_label = QLabel()
        pitch_label.setText("0")
        roll_label.setText("0")
        pitch_label.setAlignment(Qt.AlignCenter)
        roll_label.setAlignment(Qt.AlignCenter)
        pitch_label.setFrameStyle(QFrame.Panel)
        roll_label.setFrameStyle(QFrame.Panel)
        pitch_label.setLineWidth(2)
        roll_label.setLineWidth(2)
        vbox6.addWidget(pitch_label)
        vbox6.addWidget(roll_label)
        
        # get temperature and pressure group
        vbox7 = QHBoxLayout()
        group7 = QGroupBox()
        group7.setLayout(vbox7)

        temp_press = QLabel("Get Raman Temperature and Pressure")
        LED6 = LedIndicator()
        LED6.setDisabled(True)
        vbox7.addWidget(temp_press)
        vbox7.addWidget(LED6)

        # add display boxes for temperature and pressure
        temp_label = QLabel()
        press_label = QLabel()
        temp_label.setText("0")
        press_label.setText("0")
        temp_label.setAlignment(Qt.AlignCenter)
        press_label.setAlignment(Qt.AlignCenter)
        temp_label.setFrameStyle(QFrame.Panel)
        press_label.setFrameStyle(QFrame.Panel)
        temp_label.setLineWidth(2)
        press_label.setLineWidth(2)
        vbox7.addWidget(temp_label)
        vbox7.addWidget(press_label)

        # broadcast setting
        vbox8 = QHBoxLayout()
        group8 = QGroupBox()
        group8.setLayout(vbox8)

        broadcast = QLabel("Broadcast")
        LED7 = LedIndicator()
        LED7.setDisabled(True)
        LED7.on_color_1 = QColor(0,255,0)
        LED7.off_color_1 = QColor(255,0,0)
        LED7.off_color_2 = QColor(255,0,0)
        vbox8.addWidget(broadcast)
        vbox8.addWidget(LED7)

        button1 = QPushButton()
        button1.setText("Toggle")
        button1.clicked.connect(lambda: change_led(LED7))

        vbox8.addWidget(button1)

        # disk write setting
        vbox9 = QHBoxLayout()
        group9 = QGroupBox()
        group9.setLayout(vbox9)

        disk_write = QLabel("Disk Write")
        LED8 = LedIndicator()
        LED8.setDisabled(True)
        LED8.on_color_1 = QColor(0,255,0)
        LED8.off_color_1 = QColor(255,0,0)
        LED8.off_color_2 = QColor(255,0,0)
        vbox9.addWidget(disk_write)
        vbox9.addWidget(LED8)

        button2 = QPushButton()
        button2.setText("Toggle")
        button2.clicked.connect(lambda: change_led(LED8))

        vbox9.addWidget(button2)
        
        # add comprising widgets into master groupbox
        vbox1.addWidget(group10)
        vbox1.addWidget(group2)
        vbox1.addWidget(group3)
        vbox1.addWidget(group4)
        vbox1.addWidget(group5)
        vbox1.addWidget(group6)
        vbox1.addWidget(group7)
        vbox1.addWidget(group8)
        vbox1.addWidget(group9)
        
        # set the central widget of the window
        self.setCentralWidget(group1)
    
# can use fbs to make this code into a distributable executable
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    window.show()
    app.exec_()