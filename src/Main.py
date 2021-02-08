'''
Created on 20 jan. 2021

@author: edu
'''
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from MausClickerUI import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from MouseTracking import MouseTracking
from KeyboardTracking import KeyboardTracking
from ScriptRunner import ScriptRunner
import sys


class MainControl(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # Creación MouseTracking class
        self.mouseTrack = MouseTracking()
        self.keyboardTrack = KeyboardTracking()
        self.keyboardTrack.pressedKeySignal.connect(self.keyMonitorize)
        self.keyboardTrack.start()
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
        self.ui.saveBtn.setEnabled(False)

        if self.ui.coordList.rowCount() > 0:
            self.ui.playBtn.setEnabled(True)
        self.ui.playBtn.clicked.connect(self.startScript)
        self.ui.stopBtn.clicked.connect(self.activateUI)

        # Header de la tabla
        self.ui.coordList.setHorizontalHeaderLabels(("Coord X", "Coord Y", "Delay"))
        return

    def mouseGetPos(self,x,y):
        ''' Método donde a traves del Thread MouseTracking obtenemos las coordenadas
        del ratón y las asignamos al label para que se vea en tiempo real.'''
        self.x = x
        self.y = y
        self.ui.coordLbl.setText(f"Coords: {x}, {y}")

    def keyMonitorize(self, key):
        letra = str(key)

        if letra == "Key.f7":
            self.ui.playBtn.setEnabled(True)
            self.ui.saveBtn.setEnabled(True)
            #Al pulsar F7 añadimos las coordenadas a la tabla
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

        if letra == "Key.f6":
            if self.script.isRunning() == False:
                self.ui.stopBtn.setEnabled(True)
                coordList = []
                numRows = self.ui.coordList.rowCount()  # Contamos las columnas que hay
                for row in range(numRows):
                    # Por cada columna existente cogemos los valores y movemos el ratón a las posiciones con su delay.
                    coordX = self.ui.coordList.item(row, 0)
                    coordY = self.ui.coordList.item(row, 1)
                    delay = self.ui.coordList.item(row, 2)
                    coordList.append([coordX.text(), coordY.text(), delay.text()])

                self.script = ScriptRunner(coordList, int(self.ui.lineEdit.text()))
                self.script.finishSignal.connect(self.activateUI)
                self.script.start()
        if letra == "Key.f8":
            if self.script.isRunning() == True:
                self.script.stop()
                self.activateUI()

    def startScript(self):
        self.ui.stopBtn.setEnabled(True)
        self.ui.lineEdit.setEnabled(False)
        self.ui.saveBtn.setEnabled(False)
        coordList = []
        numRows = self.ui.coordList.rowCount()  # Contamos las columnas que hay
        for row in range(numRows):
            # Por cada columna existente cogemos los valores y movemos el ratón a las posiciones con su delay.
            coordX = self.ui.coordList.item(row, 0)
            coordY = self.ui.coordList.item(row, 1)
            delay = self.ui.coordList.item(row, 2)
            coordList.append([coordX.text(), coordY.text(), delay.text()])

        self.script = ScriptRunner(coordList, int(self.ui.lineEdit.text()))
        self.script.finishSignal.connect(self.activateUI)
        self.script.start()

    def activateUI(self):
        self.ui.stopBtn.setEnabled(False)
        self.ui.playBtn.setEnabled(True)
        self.ui.saveBtn.setEnabled(True)
        self.ui.lineEdit.setEnabled(True)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

app = QtWidgets.QApplication(sys.argv)
mainWindow = MainControl()
mainWindow.show()
sys.excepthook = except_hook
sys.exit(app.exec_())



