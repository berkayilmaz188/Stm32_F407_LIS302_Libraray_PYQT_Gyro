#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore,QtSvg


from PyQt5.QtCore import QTimer
from qfi import qfi_ADI, qfi_ALT, qfi_SI, qfi_HSI, qfi_VSI, qfi_TC
import math
import time
from PyQt5.QtCore import QTimer
from datetime import datetime
import  serial
import serial.tools.list_ports
import struct

i=0
g_scale = 2.0
value_scale = 255.



class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setWindowTitle("Stm Real Time Simulator")

        self.mainLayout=QVBoxLayout()
        self.upLayout=QFormLayout()
        self.layout=QGridLayout()

        self.mainLayout.addLayout(self.upLayout,30)
        self.mainLayout.addLayout(self.layout,70)

        self.port_label=QLabel("Port :")
        self.port=QComboBox()
        self.port.setStyleSheet("font-size:8pt;")
        self.list_port()
        self.frequency_label=QLabel("Frequency(Hz) :")
        self.frequency=QLineEdit()
        self.baudrate_label=QLabel("BaudRate :")
        self.baudrate=QComboBox()
        self.baudrate.addItems(["115200"])
        self.pitch=QLabel("Pitch :  ")
        self.pitch_value=QLabel("...")
        self.pitch.setStyleSheet("color:red;")
        self.pitch_value.setStyleSheet("color:red;")
        self.roll=QLabel("Roll :  ")
        self.roll_value=QLabel("...")
        self.roll.setStyleSheet("color:green;")
        self.roll_value.setStyleSheet("color:green;")

        self.btn_connect=QPushButton("Enter",self)
        self.btn_connect.clicked.connect(self.connect_system)
        
        self.btn_exit=QPushButton("Exit",self)
        self.btn_exit.clicked.connect(self.exit)

        self.upLayout.addRow(self.port_label,self.port)
        self.upLayout.addRow(self.baudrate_label,self.baudrate)
        self.upLayout.addRow(self.frequency_label,self.frequency)
        self.upLayout.addRow(self.btn_connect,self.btn_exit)
        self.upLayout.addRow(self.pitch,self.pitch_value)
        self.upLayout.addRow(self.roll,self.roll_value)
        
        self.adi = qfi_ADI.qfi_ADI(self)
        self.adi.resize(300, 300)
        self.adi.reinit()
        self.layout.addWidget(self.adi, 0, 0)

        self.setLayout(self.mainLayout)
        
        self.timer=QTimer()
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.update1)
        
        self.show()

    def convert_to_g(self, axis, raw):
        if axis == 'X' or axis == 'Y':
            if 0 <= raw <= 60:
                return raw / 60.0
            elif 60 < raw <= 200:
                return -((raw - 60) / 140.0)
            else:
                return -1 + (raw - 200) / 56.0  # 255'ten 200'e kadar olan 55 birimlik aralığı -1G'den 0'a ölçeklendiriyoruz.
        elif axis == 'Z':
            if raw == 60:
                return 1
            elif raw <= 60:
                return raw / 60.0
            else:
                return -(raw / 200.0)  # Bu kısmı değiştirmeyeceğiz, eğer Z için bu doğruysa.
        return 0





    def calculate_pitch_roll(self, g_x, g_y, g_z):
        pitch = math.atan2(g_y, math.sqrt(g_x*g_x + g_z*g_z)) * (180.0 / math.pi)
        roll = math.atan2(-g_x, g_z) * (180.0 / math.pi)
        return pitch, roll
    
    
    def update1(self):
        global i
        line = str(self.ser.readline())
        print(line)
        data = line.split(",")
        
        x_raw = float(data[0].split(":")[1])
        y_raw = float(data[1].split(":")[1])
        z_raw = float(data[2].split(":")[1].split('\\')[0])
        
        x_g = self.convert_to_g('X', x_raw)
        y_g = self.convert_to_g('Y', y_raw)
        z_g = self.convert_to_g('Z', z_raw)
        
        print(f"X_g: {x_g}, Y_g: {y_g}, Z_g: {z_g}")  # Kontrol için g değerlerini yazdır.

        pitch = math.atan2(-x_g, math.sqrt(y_g * y_g + z_g * z_g)) * (180.0 / math.pi)
        roll = math.atan2(y_g, z_g) * (180.0 / math.pi)
        
        self.pitch_value.setText(str(pitch))
        self.roll_value.setText(str(roll))
        self.adi.setRoll(roll)
        self.adi.setPitch(pitch)
        self.adi.viewUpdate.emit()



        
    def connect_system(self):
        print("Connecting System")
        self.ser = serial.Serial(self.port.currentText(), 9600)
        print(str(self.port)+" Connecting Port")
        self.timer.start()

    def list_port(self):
        ports = list(serial.tools.list_ports.comports())
        print(ports)
        for p in ports:
            print(p)
            self.port.addItems(p)

    def exit(self):
        self.timer.stop()
        sys.exit()
        

    
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

