# Gas geben mit R2, Kreis setzt Geschwindigkeit auf 0, PS-Taste beendet Motor Treiber
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

    def on_R2_press(self, value):
       speed = 0.000015625*value + 0.5
       print("Vorwaerts")
       if speed > 1:
          speed = 1
       if speed < 0:
          speed = 0
       HBridge.setSpeed(speed)
       print("Geschwindigkeit:", speed)

    def on_R2_release(self):
       print("Motor aus")
       HBridge.setSpeed(0)

    def on_circle_press(self):
       print("Speed = 0")
       HBridge.setSpeed(0)

    def on_playstation_button_press(self):
       print("Exit")
       HBridge.exit()

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)
