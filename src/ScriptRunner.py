'''
Created on 20 jan. 2021

@author: edu
'''
from PyQt5.QtCore import QThread,pyqtSignal
from pynput.mouse import Controller, Button
import time


class ScriptRunner(QThread):
    finishSignal = pyqtSignal()
    def __init__(self, coordList, loopTimes):
        QThread.__init__(self)
        #Creamos un objeto Controller que nos permitirá trackear el ratón
        self.mouse = Controller()
        self.coordList = coordList
        self.loopTimes = loopTimes
    def __del__(self):
        self.wait()

    def run(self):
        for i in range(self.loopTimes):
            for row in range(len(self.coordList)):
                # Por cada columna existente cogemos los valores y movemos el ratón a las posiciones con su delay.
                time.sleep(int(self.coordList[row][2]) / 1000)
                self.mouse.position = (int(self.coordList[row][0]), int(self.coordList[row][1]))
                self.mouse.click(Button.left, 1)
        self.finishSignal.emit()
    def stop(self):
        self.terminate()
        self.exit()
        self.finishSignal.emit()
