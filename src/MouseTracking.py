'''
Created on 20 jan. 2021

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

    '''
    mouse = Controller()

    # Read pointer position
    print('The current pointer position is {0}'.format(
        mouse.position))

    # Set pointer position
    mouse.position = (10, 20)
    print('Now we have moved it to {0}'.format(
        mouse.position))

    # Move pointer relative to current position
    mouse.move(5, -5)

    # Press and release
    mouse.press(Button.left)
    mouse.release(Button.left)

    # Double click; this is different from pressing and releasing
    # twice on macOS
    mouse.click(Button.left, 2)

    # Scroll two steps down
    mouse.scroll(0, 2)
    '''