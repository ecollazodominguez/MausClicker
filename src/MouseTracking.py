'''
Created on 27 jan. 2021

@author: edu
'''
from PyQt5.QtCore import QThread,pyqtSignal
from pynput.mouse import Controller


class MouseTracking(QThread):
    my_signal = pyqtSignal('PyQt_PyObject','PyQt_PyObject')
    def __init__(self):
        QThread.__init__(self)
        #Creamos un objeto Controller que nos permitirá trackear el ratón
        self.mouse = Controller()
        self.mousePos = self.mouse.position
    def __del__(self):
        self.wait()

    def run(self):
        while(True):
            # Mientras el Thread esté activo y la posición del ratón sea diferente se guardará la nueva posición y se mandará como señal.
            if self.mousePos != self.mouse.position:
                self.mousePos = self.mouse.position
                self.my_signal.emit(self.mousePos[0],self.mousePos[1])