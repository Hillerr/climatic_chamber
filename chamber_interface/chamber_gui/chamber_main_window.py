# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from .routine import RoutineManager 
from .gui_setup import Ui_MainWindowSetup
from .temp_plot import MatplotWidget
        

class ChamberMainWindow(QtWidgets.QMainWindow, Ui_MainWindowSetup):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()

        self.target_temp = None
        self.curr_temp = None
        self.time_remaining = {
            "hour": "--",
            "minute": "--",
            "second": "--"
        }
        self.routine_manager = RoutineManager()

        self.setupUi(self)
        self.init_widget()
        self.configure_events()

        
    def init_widget(self):
        self.matplotlib_widget = MatplotWidget()
        self.layoutvertical = QtWidgets.QVBoxLayout(self.plot_widget)
        self.layoutvertical.addWidget(self.matplotlib_widget)


    def configure_events(self):
        self.actionNew_routine.triggered.connect(self.routine_manager.new_routine)
        self.actionOpen_routine.triggered.connect(self.routine_manager.open_routine)
        self.stop_button.clicked.connect(self.routine_manager.end_routine)
        self.configure_timers()


    def configure_timers(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update)
        self.timer.start()


    def update(self):
        if self.routine_manager.status == True:
            self.routine_manager.update()
            self.curr_temp = self.routine_manager.get_current_temp()
            self.target_temp = self.routine_manager.get_target_temp() 

            if self.routine_manager.status == True:
                self.time_remaining = self.routine_manager.get_period_remaining()           
                     
            self.update_plot()
            self.update_temp_labels()
            self.update_state()
            self.update_remaining_time()
            
            self.conn_status_value.setText("Connected")
            if self.server_ip_label_value.text() == "--":
                self.server_ip_label_value.setText(self.routine_manager.ip)
        


    def update_temp_labels(self):
        self.update_target_temp()
        self.update_current_temp()


    def update_plot(self):
        self.matplotlib_widget.update_plot(self.curr_temp, self.target_temp)


    def update_current_temp(self):
        self.curr_temp_value.setText(f"{self.curr_temp} °C")


    def update_target_temp(self):
        self.target_temp_value.setText(f"{self.target_temp} °C")


    def update_state(self):
        if self.routine_manager.transient:
            self.state_value.setText("Transition")
            self.state_value.setStyleSheet("Color: Red")

        elif self.routine_manager.transient == False:
            self.state_value.setText("Steady")
            self.state_value.setStyleSheet("Color: Green")

        elif self.routine_manager.status == False:
            self.state_value.setText("Off")
            self.state_value.setStyleSheet("Color: Gray")


    def update_remaining_time(self):
        self.time_remaining_value.setText(
            f"{self.time_remaining['hour']:02d} : {self.time_remaining['minute']:02d} : {self.time_remaining['second']:02d}"
        )

    
    def update_room_temp(self):
        pass


    def disconnect(self):
        self.conn_status_value.setText("Disconnected")
        self.conn_status_value.setStyleSheet("color: Red")