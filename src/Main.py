'''
Created on 20 jan. 2021

@author: edu
'''
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from MausClickerUI import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from MouseTracking import MouseTracking
from pynput.mouse import Controller, Button
import time
import sys


class MainControl(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # Creación MouseTracking class
        self.mouseTrack = MouseTracking()
        self.mouseTrack.start()
        # Señal del Thread que llamará el método MouseGetPos
        self.mouseTrack.my_signal.connect(self.mouseGetPos)

        # Creacion objetos ventana grafica
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initialization()

    def initialization(self):

        # Botones
        self.ui.stopBtn.setEnabled(False)
        self.ui.playBtn.setEnabled(False)

        if self.ui.coordList.rowCount() > 0:
            self.ui.playBtn.setEnabled(True)
        self.ui.playBtn.clicked.connect(self.startScript)

        # Header de la tabla
        self.ui.coordList.setHorizontalHeaderLabels(("Coord X", "Coord Y", "Delay"))
        return

    def mouseGetPos(self,x,y):
        ''' Método donde a traves del Thread MouseTracking obtenemos las coordenadas
        del ratón y las asignamos al label para que se vea en tiempo real.'''
        self.x = x
        self.y = y
        self.ui.coordLbl.setText(f"Coords: {x}, {y}")

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_F7:
            self.ui.playBtn.setEnabled(True)
            '''Al pulsar F7 añadimos las coordenadas a la tabla'''
            numRows = self.ui.coordList.rowCount() #Contamos las columnas que hay
            self.ui.coordList.insertRow(numRows) #Añadimos una nueva columna en función de las que haya

            # Añadimos coordenadas X, Y y un delay fijo
            self.ui.coordList.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(self.x)))
            self.ui.coordList.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(self.y)))
            self.ui.coordList.setItem(numRows, 2, QtWidgets.QTableWidgetItem("2000"))

            # Centramos los datos
            self.ui.coordList.item(numRows,0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.coordList.item(numRows, 1).setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.coordList.item(numRows, 2).setTextAlignment(QtCore.Qt.AlignCenter)

        if qKeyEvent.key() == QtCore.Qt.Key_F6:
            self.ui.stopBtn.setEnabled(True)
            numRows = self.ui.coordList.rowCount()  # Contamos las columnas que hay
            mouse = Controller() #Creamos un controller del raton
            for row in range(numRows):
                # Por cada columna existente cogemos los valores y movemos el ratón a las posiciones con su delay.
                coordX = self.ui.coordList.item(row,0)
                coordY = self.ui.coordList.item(row, 1)
                delay = self.ui.coordList.item(row, 2)
                time.sleep(int(delay.text())/1000)
                mouse.position = (int(coordX.text()),int(coordY.text()))
                mouse.click(Button.left, 1)
    def startScript(self):
        #TODO THREAD
        self.ui.stopBtn.setEnabled(True)
        numRows = self.ui.coordList.rowCount()  # Contamos las columnas que hay
        mouse = Controller()  # Creamos un controller del raton
        for row in range(numRows):
            # Por cada columna existente cogemos los valores y movemos el ratón a las posiciones con su delay.
            coordX = self.ui.coordList.item(row, 0)
            coordY = self.ui.coordList.item(row, 1)
            delay = self.ui.coordList.item(row, 2)
            time.sleep(int(delay.text()) / 1000)
            mouse.position = (int(coordX.text()), int(coordY.text()))
            mouse.click(Button.left, 1)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

app = QtWidgets.QApplication(sys.argv)
mainWindow = MainControl()
mainWindow.show()
sys.excepthook = except_hook
sys.exit(app.exec_())



