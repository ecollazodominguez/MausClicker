'''
Created on 27 ago. 2020

@author: enxenia
'''

from pynput import keyboard  # sudo pip install pynput
from PyQt5.QtCore import QThread,pyqtSignal



class KeyboardTracking(QThread):
    pressedKeySignal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        self.pressedKeySignal.emit(key)