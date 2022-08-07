# Steuerkreuz nach oben -> 10% vorwärts
# Steuerkreuz nach unten -> 10% rückwärts
# nach dem loslassen stoppt der Motor
from pyPS4Controller.controller import Controller

#importiere verschiedene Python Klassen
import sys, tty, termios, os

# Das Programm BTS7960HBridgePCA9685.py wird als Modul geladen. Es stellt
# die Funktionen fuer die Steuerung der H-Bruecke zur Verfuegung.
# definierte Funktionen sind:
# "setMode(mode)" mode ist aus {reverse, forward}
# "setSpeed(power)" power ist aus {-1,1}
# "exit()" Pins aus, PWM aus
import BTS7960HBridgePCA9685 as HBridge

print("Strg + C zum beenden")

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_up_arrow_press(self):
       print("Vorwaerts 10%")
       HBridge.setSpeed(0.1)

    def on_down_arrow_press(self):
       print("Rueckwärts 10%")
       HBridge.setSpeed(-0.1)

    def on_up_down_arrow_release(self):
       print("Motor aus")
       HBridge.setSpeed(0)

    def on_circle_press(self):
       print("Exit")
       HBridge.exit()

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)
