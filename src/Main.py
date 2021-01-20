'''
Created on 20 jan. 2021

@author: edu
'''
from PyQt5 import QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from MausClickerUI import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from MouseTracking import MouseTracking
import sys


class MainControl(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # Creación MouseTracking class
        self.mouse = MouseTracking()
        self.mouse.start()
        self.mouse.my_signal.connect(self.mouseGetPos)

        # Creacion objetos ventana grafica
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initialization()

    def initialization(self):

        # Botones
        self.ui.stopBtn.setEnabled(False)
        self.ui.playBtn.setEnabled(False)
        return

    def mouseGetPos(self,x,y):
        self.ui.coordLbl.setText(f"Coords: {x}, {y}")


app = QtWidgets.QApplication(sys.argv)
mainWindow = MainControl()
mainWindow.show()
sys.exit(app.exec_())


