import sys
import time
import numpy as np
from PyQt5 import  QtGui, QtCore,QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import serial
import serial.tools.list_ports
import pyqtgraph as pg
import datetime
from scipy import stats


######################################################################################### Start of the code

isSerialReading = True

class ibiSignals(QObject): # PyQT Signals for IBI sequence Thread
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class serialSignals(QObject): #PyQt Signals for Serial Read Thread
    start_signal = pyqtSignal()
    mode_signal = pyqtSignal(int)

class sensor_serialSignals(QObject): #PyQt Signals for Serial Read Thread
    data_signal = pyqtSignal(str)

class serialRead(QRunnable):  # a Thread for serial read loop to avoid freeze

    def __init__(self):
        super(serialRead, self).__init__()
        self.signals = serialSignals()

    @pyqtSlot()
    def stop(self):
        return

    @pyqtSlot()
    def run(self):
        while(True):#
            data = sync_ser.read(1) #read a byte
            if len(data) > 0:
                status = int.from_bytes(data, byteorder='big')
                print(status)
                # if status == 5: # if signal equals to 5 send a PyQt signal
                #     self.signals.start_signal.emit()
                # else:
                #     self.signals.mode_signal.emit(status)

class HR_serialRead(QRunnable):  # a Thread for serial read loop to avoid freeze

    def __init__(self):
        super(HR_serialRead, self).__init__()
        self.signals = sensor_serialSignals()
        self.i = 0
    @pyqtSlot()
    def stop(self):
        return

    @pyqtSlot()
    def run(self):
        while(True):#
            line = HR_ser.readline().decode("utf-8")
            if len(line) > 2 and "B" or "S" in line:
                self.signals.data_signal.emit(line[:-1])


class GSR_serialRead(QRunnable):  # a Thread for serial read loop to avoid freeze

    def __init__(self):
        super(GSR_serialRead, self).__init__()
        self.signals = sensor_serialSignals()

    @pyqtSlot()
    def stop(self):
        return

    @pyqtSlot()
    def run(self):
        while(True):
            data = GSR_ser.readline().decode("utf-8") # read a byte
            if len(data) > 2:
                self.signals.data_signal.emit(data[:-1])


class ApplicationWindow(QtWidgets.QMainWindow): # Main class of the Application
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('./resource/icon.png'))

        # self.ibis_thread = QThreadPool() # Initiate IBI Thread Pool
        self.sync_thread= QThreadPool() # Initiate Serial Thread Pool
        self.HR_thread = QThreadPool()
        self.GSR_thread = QThreadPool()
        self._title = 'DolyREC BioRecorder' # Title of the app
        self.setWindowTitle(self._title)
        self.setStyleSheet("QMainWindow{background: gray url(./resource/logo_w1.png) no-repeat; background-position: left top;margin-left:50%;margin-top:50%}") # Set background color and logo image

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main) # set the main widget

        self.formGroupBox = QGroupBox("Form") # a form box at the left side
        self.formGroupBox.setMaximumHeight(600) #set form height
        self.formGroupBox.setFixedWidth(400)    #set form width
        form_layout = QFormLayout()# Initiate PyQt form layout
        form_layout.setSpacing(1)# space between each item

        self.subject_id = QLineEdit() # The Text box for subject ID
        self.subject_id.setText("999") # set subject id to 999
        self.subject_id.textChanged.connect(self.check_input) # Send signal to check_input function when subject_id changes

        self.name = QLineEdit() # The Text box for subject ID
        # self.name.setText() # set subject id to 999
        self.name.textChanged.connect(self.check_input) # Send signal to check_input function when subject_id changes


        self.age = QSpinBox() #
        # self.age.valueChanged.connect(self.check_increment_duration)
        self.age.setMaximum(110)
        self.age.setValue(15)

        self.gender = QComboBox(self)
        self.gender.addItem("Male")
        self.gender.addItem("Female")

        self.status_box = QTextBrowser() # Status Box
        self.status_box.setText("Please input the Subject ID and the name")
        self.status_box.setMaximumHeight(50)

        self.button_start = QtWidgets.QPushButton('Run', self) # Run button
        self.button_start.setDisabled(True)
        self.button_start.clicked.connect(self.Run_button) #Connect to self.Run_button Function

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button_start) # add button an horizontal layout

        # add all widgets to from layout
        form_layout.addRow(QLabel("Subject ID: "),self.subject_id)
        form_layout.addRow(QLabel("Name: "), self.name)
        form_layout.addRow(QLabel("Age: "), self.age)
        form_layout.addRow(QLabel("Gender: "), self.gender)
        form_layout.addRow(QLabel("Status: "), self.status_box)
        form_layout.addRow(self.button_layout)
        self.formGroupBox.setLayout(form_layout)

        # Initiate PPG Plot
        self.PPG_Plot = pg.PlotWidget(title= "PPG　Time Series")
        self.PPG_Plot.hideAxis('bottom')
        self.PPG_Plot.setMouseEnabled(x=False, y=True)
        self.PPG_Plot.setRange(yRange=(200, 800), padding=0)

        # Initiate HR Plot
        self.HR_Plot = pg.PlotWidget(title= "HR　Time Series")
        self.HR_Plot.setMouseEnabled(x=False, y=True)
        self.HR_Plot.setRange(yRange=(60, 140), padding=0)

        self.GSR_Plot = pg.PlotWidget(title= "GSR　Time Series")
        self.GSR_Plot.setMouseEnabled(x=False, y=True)
        self.GSR_Plot.hideAxis('bottom')
        self.GSR_Plot.setRange(yRange=(0, 600), padding=0)

        # creating label
        # self.label = QLabel(self)
        # self.pixmap = QPixmap('./resource/image.png')
        # self.label.setPixmap(self.pixmap)

        # main layouts
        layout = QtWidgets.QGridLayout(self._main)
        self.sensor_widget = QtWidgets.QLabel(alignment=QtCore.Qt.AlignRight)
        self.sensor_widget.setFixedHeight(140)
        self.sensor_widget.setFixedWidth(100)
        sensor_layout = QtWidgets.QVBoxLayout()
        # add form layout and plots to the main grid layout
        layout.addWidget(self.HR_Plot, 0, 1,1,4)
        layout.addWidget(self.PPG_Plot, 1, 1,1,4)
        layout.addWidget(self.GSR_Plot, 2, 1, 1, 4)
        layout.addWidget(self.formGroupBox, 1, 0,4,1)

        # sensor_layout.addWidget(self.sensor_widget)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        self.keyPressEvent = self._key_pressed # set key press event for Exit and Etc.

        self.hr_serialRead = HR_serialRead()
        self.hr_serialRead.signals.data_signal.connect(lambda signal: self.HR_update_value(signal))
        self.HR_thread.start(self.hr_serialRead)

        self.gsr_serialRead = GSR_serialRead()
        self.gsr_serialRead.signals.data_signal.connect(lambda signal: self.GSR_update_value(signal))
        self.GSR_thread.start(self.gsr_serialRead)
        if not debug:
            self.sync_serialRead = serialRead()
            self.sync_serialRead.signals.start_signal.connect(self.Run_button)
            self.sync_serialRead.signals.mode_signal.connect(lambda signal: self.sync_signal(signal))
            self.sync_thread.start(self.sync_serialRead)

################################################################################ Intialize Variables for the Experiment
        self.subject_IDname = ""
        self.subject_name = ""
        self.sync_status = -1
        #HR and PPG buffer lists
        self.PPG_data = []
        self.HR_data = []
        self.HR_Time = list(range(1,31))
        self.GSR_data = []
        # HR csv record
        self.HR_record_fileName = ""
        self.PPG_record_fileName = ""
        self.GSR_record_fileName = ""
        self.record_path= "./Record/"
        self.isRecording = False

################################################################################
    def sync_signal(self,status):
        if self.sync_status == -1 and status==0 :
            self.Run_button()
            self.sync_status = status
        elif status == 255:
            self.Run_button()
        else:
            self.sync_status = status

    def create_record(self):

        x = datetime.datetime.now()
        time = x.strftime("%Y-%m-%d_%H-%M-%S")
        self.HR_record_fileName =self.record_path + self.subject_IDname + "_" + time + "_HR.csv"
        self.PPG_record_fileName = self.record_path + self.subject_IDname + "_" + time + "_PPG.csv"
        self.GSR_record_fileName = self.record_path + self.subject_IDname + "_" + time + "_GSR.csv"

        record_file_HR= open(self.HR_record_fileName,"w")
        record_file_HR.write("Time,HR,Status\n".format(time,self.subject_IDname))
        record_file_HR.close()

        record_file_GSR= open(self.GSR_record_fileName,"w")
        record_file_GSR.write("Time,GSR,Status\n".format(time,self.subject_IDname))
        record_file_GSR.close()

        record_file_PPG= open(self.PPG_record_fileName,"w")
        record_file_PPG.write("Time,PPG,Status\n".format(time,self.subject_IDname))
        record_file_PPG.close()
        self.isRecording = True

    # Write HR values to the csv file
    def record_HR(self,time,hr,status):
        file = open(self.HR_record_fileName,"a")
        file.write("{0},{1},{2}\n".format(time,hr,status))
        file.close()

    def record_PPG(self,time,ppg,status):
        file = open(self.PPG_record_fileName,"a")
        file.write("{0},{1},{2}\n".format(time,ppg,status))
        file.close()
    def record_GSR(self,time,gsr,status):
        file = open(self.GSR_record_fileName,"a")
        file.write("{0},{1},{2}\n".format(time,gsr,status))
        file.close()
    def _key_pressed(self,e):
        if e.key() == Qt.Key_Q:
            self.close()

    def Disable_Form(self,boolean):
        bool = False
        if boolean == False:
            bool = True

        self.subject_id.setEnabled(bool)
        self.pulse_sensor_checkbox.setEnabled(bool)
        self.mod1.setEnabled(bool)
        self.mod2.setEnabled(bool)
        self.mod3.setEnabled(bool)
        self.initial_bpm_box.setEnabled(bool)
        self.task_increment_duration_box.setEnabled(bool)
        self.task_vibrate_time_box.setEnabled(bool)
        self.HR_increment_box.setEnabled(bool)

    # disable or enable intial HR value based on pulse sensor check box
    def check_pulse_sesnor_usage(self):

        if self.pulse_sensor_checkbox.isChecked():
            self.use_pulse_sensor = True
            self.initial_bpm_box.setEnabled(False)
        else:
            if self.mod != 1:
                self.use_pulse_sensor = False
                self.initial_bpm_box.setEnabled(True)

    # Update mode based the user input
    def update_mode(self,value):
        rbtn = self.sender()
        if rbtn.isChecked() == True:
            mode_val = int(rbtn.text()[-1])
            self.mod = mode_val
            if mode_val == 1:
                #self.pulse_sensor_checkbox.setChecked(False)
                # self.use_pulse_sensor = False
                # self.pulse_sensor_checkbox.setEnabled(False)
                self.task_increment_duration_box.setEnabled(False)
                self.HR_increment_box.setEnabled(False)
                self.initial_bpm_box.setEnabled(False)

            elif mode_val == 2:
                self.task_increment_duration_box.setValue(0)
                self.pulse_sensor_checkbox.setEnabled(True)
                self.task_increment_duration_box.setEnabled(False)
                self.HR_increment_box.setEnabled(True)

            elif mode_val == 3:
                self.task_increment_duration_box.setValue(60)
                self.pulse_sensor_checkbox.setEnabled(True)
                self.task_increment_duration_box.setEnabled(True)
                self.HR_increment_box.setEnabled(True)
            self.check_input()


    # Check all values have been entered
    def check_input(self):
        self.subject_IDname = self.subject_id.text()
        self.subject_name= self.name.text()
        if self.subject_id.text() != "" and self.name.text() != "":
            self.button_start.setDisabled(False)
            self.status_box.setText("Please Click on Run Button to Start!")
        else:
            self.button_start.setDisabled(True)
            self.status_box.setText("Please enter the Subject ID and Name")

    # Run button function to start the task
    def Run_button(self):

        if self.isRecording:
            print("trying to reset")
            self.Reset()
        print(self.isRecording)
        self.create_record()
        self.status_box.setText("Recording Started! Send Trigger using the serial port")
        self.button_start.setText("Stop")

    # save subject info reset variables for next subject
    def Reset(self):
        print("Reset")
        self.button_start.setText("Run")
        self.status_box.setText("Recording Stopped!")
        self.isRecording = False
        self.sync_status = -1


    # get values from Pulse Sensor (Arduino)
    def HR_update_value(self,data):
        x = list(range(500))
        x1=list(range(30))
        line = data
        if len(line)> 2:
            data_type = line[0]
            value = int(line[1:])
            len_PPG = len(self.PPG_data)
            len_HR = len(self.HR_data)
            #print(str(self.mod_group.sender()))
            if (data_type == "S"):

                if(len_PPG < 499):
                    self.PPG_data.append(value)

                elif (len_PPG == 499):
                    self.PPG_data.append(value)
                    self.PPG_Plot.plot(x, self.PPG_data)

                elif(len_PPG == 500):
                    self.PPG_data = self.PPG_data[1:]
                    self.PPG_data.append(value)
                    self.PPG_Plot.clear()
                    self.PPG_Plot.plot(x, self.PPG_data)

                if (self.isRecording == True):
                    x_time = datetime.datetime.now()
                    time = x_time.strftime("%H:%M:%S.%f")
                    self.record_PPG(time,value,self.sync_status)

            elif (data_type == "B"):

                if (len_HR < 29):
                    self.HR_data.append(value)

                elif (len_HR == 29):
                    self.HR_data.append(value)
                    self.HR_Plot.plot(x1, self.HR_data)

                elif (len_HR == 30):
                    self.HR_data = self.HR_data[1:]
                    self.HR_Time = self.HR_Time[1:]
                    self.HR_Time.append(self.HR_Time[28]+1)
                    self.HR_data.append(value)
                    self.HR_Plot.clear()
                    self.HR_Plot.plot(self.HR_Time, self.HR_data)

                if (self.isRecording == True):
                    x_time = datetime.datetime.now()
                    time = x_time.strftime("%H:%M:%S.%f")
                    self.record_HR(time,value,self.sync_status)
    def GSR_update_value(self,data):
        x = list(range(250))
        value = int(data)
        len_GSR = len(self.GSR_data)

        if (self.isRecording == True):
            x_time = datetime.datetime.now()
            time = x_time.strftime("%H:%M:%S.%f")
            self.record_GSR(time, value, self.sync_status)

        if(len_GSR < 249):
            self.GSR_data.append(value)

        elif (len_GSR == 249):
            self.GSR_data.append(value)
            self.GSR_Plot.plot(x, self.GSR_data)

        elif(len_GSR == 250):
            self.GSR_data = self.GSR_data[1:]
            self.GSR_data.append(value)
            self.GSR_Plot.clear()
            self.GSR_Plot.plot(x, self.GSR_data)

        if (self.isRecording == True):
            x = datetime.datetime.now()
            time = x.strftime("%H:%M:%S.%f")
            self.record_PPG(time,value,0)


class SettingDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(SettingDialog, self).__init__(*args, **kwargs)

        self.setWindowIcon(QtGui.QIcon('./resource/icon.png'))
        self.arduino_ports = []
        self.serial_ports = []

        self.serial_timer = QtCore.QTimer(self) # Initiate Timer for HR計測
        self.serial_timer.timeout.connect(self.check_serialPorts) # Connect the timer to HR計測 function

        self.setWindowTitle("Settings")
        self.formGroupBox = QGroupBox("Serial Connection Settings")
        self.formGroupBox.setMaximumHeight(600)
        self.formGroupBox.setFixedWidth(400)
        form_layout = QFormLayout()
        form_layout.setSpacing(4)
        self.serial_checkbox = QCheckBox()
        self.serial_checkbox.stateChanged.connect(self.isSerial_connection)

        self.HR_arduino_com = QComboBox(self)
        self.GSR_arduino_com = QComboBox(self)

        self.psychopy_com = QComboBox(self)
        self.psychopy_com.setDisabled(True)

        self.button_confirm = QtWidgets.QPushButton('Run', self)  # Run button
        self.button_confirm.setDisabled(True)
        self.button_confirm.clicked.connect(self.set_ports)

        form_layout.addRow("HR COM Port Number：",self.HR_arduino_com)
        form_layout.addRow("GSR COM Port Number：", self.GSR_arduino_com)
        form_layout.addRow("Serial Sync： ",self.serial_checkbox)
        form_layout.addRow("Serial COM Port Number：", self.psychopy_com)
        form_layout.addRow(self.button_confirm)
        self.serial_timer.start(100)
        self.formGroupBox.setLayout(form_layout)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.formGroupBox)
        self.setLayout(self.main_layout)

    def isSerial_connection(self):
        global debug
        if self.serial_checkbox.isChecked():
            self.psychopy_com.setDisabled(False)
            debug = False
        else:
            self.psychopy_com.setDisabled(True)
            debug = True

    def check_serialPorts(self):
        for p in serial.tools.list_ports.comports():

            if 'arduino' in p.description.lower():
                if p.device not in self.arduino_ports:
                    self.arduino_ports.append(p.device)
                    self.HR_arduino_com.addItem(p.device)
                    self.GSR_arduino_com.addItem(p.device)

            else:
                if p.device not in self.serial_ports:
                    self.serial_ports.append(p.device)
                    self.psychopy_com.addItem(p.device)
        HR_port = str(self.HR_arduino_com.currentText())
        GSR_port = str(self.GSR_arduino_com.currentText())
        psychopy_port = str(self.psychopy_com.currentText())

        if HR_port != "" and GSR_port != "" and HR_port != GSR_port:
            if debug == False:
                if psychopy_port != "":
                    self.button_confirm.setDisabled(False)
                else:
                    self.button_confirm.setDisabled(True)
            else:
                self.button_confirm.setDisabled(False)
        else:
            self.button_confirm.setDisabled(True)


    def set_ports(self):
        global com_number_HR
        global com_number_sync
        global com_number_GSR
        com_number_HR = str(self.HR_arduino_com.currentText())
        com_number_sync = str(self.psychopy_com.currentText())
        com_number_GSR =str(self.GSR_arduino_com.currentText())
        #self.flashSplash()
        self.serial_timer.stop()
        self.close()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    com_number_HR = None
    com_number_GSR = None
    com_number_sync = None
    debug = True
    setting_dlg = SettingDialog()
    setting_dlg.exec_()

    # Serial connection for arduino
    HR_ser = serial.Serial(com_number_HR, 115200, timeout=1)
    GSR_ser = serial.Serial(com_number_GSR, 9600, timeout=1)
      # Turn it to false to run without psychopy serial connection
    if not debug:
        # Serial Connection for psychopy
        sync_ser = serial.Serial(com_number_sync)
    print(com_number_sync)
    if com_number_sync != None:
        splash = QSplashScreen(QPixmap('./resource/splash.png'))
        splash.show()
        time.sleep(1.5)
        splash.close()
        app = ApplicationWindow()
        app.show()
        sys.exit(qapp.exec_())