"""
isolatedDAC.py: This program is meant to replace the old DAC.py file as a more isolated program. This program will be strictly displaying and monitoring the data acquisition process and NOt focusing on displaying data.
"""

from PyQt5.QtWidgets import QApplication
from LedIndicatorWidget import *

__author__ = "Spencer Pollard"
__credits__ = ["Spencer Pollard", "Shane Mayor"]

def change_led(LED):
    LED.setChecked(not LED.isChecked())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # main window settings
        self.setWindowTitle("LiDAR Data Acquisition Software")

        # menu bar configuration
        menu_bar = self.menuBar()
        menu_bar.addMenu('File')


        # main groupbox for the window
        # overall group for different data acquisition processes
        group1 = QGroupBox("Status of Data Acquisition")
        vbox1 = QVBoxLayout()
        group1.setLayout(vbox1)

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

        # get pulse energy group
        vbox4 = QHBoxLayout()
        group4 = QGroupBox()
        group4.setLayout(vbox4)

        pulse_energy = QLabel("Get Pulse Energy")
        LED3 = LedIndicator()
        LED3.setDisabled(True)
        vbox4.addWidget(pulse_energy)
        vbox4.addWidget(LED3)
        
        # get date/time group
        vbox5 = QHBoxLayout()
        group5 = QGroupBox()
        group5.setLayout(vbox5)

        date_time = QLabel("Get Date and Time")
        LED4 = LedIndicator()
        LED4.setDisabled(True)
        vbox5.addWidget(date_time)
        vbox5.addWidget(LED4)

        # get Pitch and Roll group
        vbox6 = QHBoxLayout()
        group6 = QGroupBox()
        group6.setLayout(vbox6)

        pitch_roll = QLabel("Get Pitch and Roll")
        LED5 = LedIndicator()
        LED5.setDisabled(True)
        vbox6.addWidget(pitch_roll)
        vbox6.addWidget(LED5)
        
        # get temp and pressure group
        vbox7 = QHBoxLayout()
        group7 = QGroupBox()
        group7.setLayout(vbox7)

        temp_press = QLabel("Get Raman Tempertature and Pressure")
        LED6 = LedIndicator()
        LED6.setDisabled(True)
        vbox7.addWidget(temp_press)
        vbox7.addWidget(LED6)

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