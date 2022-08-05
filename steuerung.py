#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20170616
# Version:   1.0
# Homepage:   http://custom-build-robots.com
# Dieses Programm ist das sogenannte Steuerprogramm fuer das Roboter
# Auto ueber die Konsole und Tastatur vom PC aus.


# Es werden verschiedene Python Klassen importiert deren Funktionen
# im Programm benoetigt werden fuer die Programmverarbeitung.
import sys, tty, termios, os, readchar

from __future__ import division
import time

from pyPS4Controller.controller import Controller
import Adafruit_PCA9685
# Das Programm BTS7960HBridgePCA9685.py wird als Modul geladen. Es stellt
# die Funktionen fuer die Steuerung der H-Bruecke zur Verfuegung.
import BTS7960HBridgePCA9685 as HBridge

# Variablen Definition der linken und rechten Geschwindigkeit der
# Motoren des Roboter-Autos.
speedleft = 0
speedright = 0

left = 0 #Linker Stick - Lenken links
left_percent = 100*up/40000 #Umrechnung in %
left_servo = 375+225*left_percent
rigth = 0 #Linker Stick - Lenken rechts
right_percent = 100*up/40000 #Umrechnung in %
right_servo = 375-225*right_percent
right_bumper = 0 #R2 - Gas
right_bumper_percent = 100*up/40000 #Umrechnung in %


# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
servo_middle = 375 #mittlere Position (geradeaus)

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)
    
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

########### PS4 code
class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
       print("läuft (X gedrückt)")

    def on_R2_press(self, value):
       right_bumper=value #R2 wert bekommen

    def on_L3_up(self, value):
       up=value #Wert vom linken Stick für "oben"
        
    def on_L3_down(self, value):
       down=value #Wert vom linken Stick für "oben"
############
print('Test Controller. Drücke X')

# Das Menue fuer den Anwender wenn er das Programm ausfuehrt.
# Das Menue erklaert mit welchen Tasten das Auto gesteuert wird.
print("R2 zum Beschleunigen")
print("Linker Stick zum Lenken")
print("q: stoppt die Motoren")
print("x: Programm beenden")

# Die Funktion getch() nimmt die Tastatureingabe des Anwenders
# entgegen. Die gedrueckten Buchstaben werden eingelesen. Sie werden
# benoetigt um die Richtung und Geschwindigkeit des Roboter-Autos
# festlegen zu koennen.
def getch():
   ch = readchar.readchar()
   return ch

# Die Funktion printscreen() gibt immer das aktuelle Menue aus
# sowie die Geschwindigkeit der linken und rechten Motoren wenn
# es aufgerufen wird.
def printscreen():
   # der Befehl os.system('clear') leert den Bildschirmihalt vor
   # jeder Aktualisierung der Anzeige. So bleibt das Menue stehen
   # und die Bildschirmanzeige im Terminal Fenster steht still.
   os.system('clear')
   print("w/s: beschleunigen")
   print("a/d: lenken")
   print("q:   stoppt die Motoren")
   print("x:   Programm beenden")
   print("========== Geschwindigkeitsanzeige ==========")
   print "Geschwindigkeit linker Motor:  ", speedleft
   print "Geschwindigkeit rechter Motor: ", speedright

# Diese Endlosschleife wird erst dann beendet wenn der Anwender 
# die Taste X tippt. Solange das Programm laeuft wird ueber diese
# Schleife die Eingabe der Tastatur eingelesen.
while True:
   # Mit dem Aufruf der Funktion getch() wird die Tastatureingabe 
   # des Anwenders eingelesen. Die Funktion getch() liesst den 
   # gedrueckte Buchstabe ein und uebergibt diesen an die 
   # Variablechar. So kann mit der Variable char weiter 
   # gearbeitet werden.
   char = getch()
   
   # Das Roboter-Auto faehrt vorwaerts wenn der Anwender die 
   # Taste "w" drueckt.
   if(char == "w"):
      # das Roboter-Auto beschleunigt in Schritten von 10% 
      # mit jedem Tastendruck des Buchstaben "w" bis maximal 
      # 100%. Dann faehrt es maximal schnell vorwaerts.
      speedleft = speedleft + 0.1
      speedright = speedright + 0.1

      if speedleft > 1:
         speedleft = 1
      if speedright > 1:
         speedright = 1
      # Dem Programm L298NHBridge welches zu beginn  
      # importiert wurde wird die Geschwindigkeit fuer 
      # die linken und rechten Motoren uebergeben.
      HBridge.setMotor(speedleft)
      printscreen()

   # Das Roboter-Auto faehrt rueckwaerts wenn die Taste "s" 
   # gedrueckt wird.
   if(char == "s"):
      # das Roboter-Auto bremst in Schritten von 10% 
      # mit jedem Tastendruck des Buchstaben "s" bis maximal 
      # -100%. Dann faehrt es maximal schnell rueckwaerts.
      speedleft = speedleft - 0.1
      speedright = speedright - 0.1

      if speedleft < -1:
         speedleft = -1
      if speedright < -1:
         speedright = -1
         
      # Dem Programm L298NHBridge welches zu beginn  
      # importiert wurde wird die Geschwindigkeit fuer 
      # die linken und rechten Motoren uebergeben.      
      HBridge.setMotor(speedleft)
      printscreen()

    # mit dem druecken der Taste "q" werden die Motoren angehalten
   if(char == "q"):
      speedleft = 0
      speedright = 0
      HBridge.setMotor(0)
      printscreen()

   # Mit der Taste "d" lenkt das Auto nach rechts bis die max/min
   # Geschwindigkeit der linken und rechten Motoren erreicht ist.
   if(char == "d"):      
      speedright = speedright - 0.1
      speedleft = speedleft + 0.1
      
      if speedright < -1:
         speedright = -1
      
      if speedleft > 1:
         speedleft = 1
      
      HBridge.setMotor(speedleft)
      printscreen()
      
   # Mit der Taste "a" lenkt das Auto nach links bis die max/min
   # Geschwindigkeit der linken und rechten Motoren erreicht ist.
   if(char == "a"):
      speedleft = speedleft - 0.1
      speedright = speedright + 0.1
         
      if speedleft < -1:
         speedleft = -1
      
      if speedright > 1:
         speedright = 1
      
      HBridge.setMotor(speedleft)
      printscreen()
      
   # Mit der Taste "x" wird die Endlosschleife beendet 
   # und das Programm wird ebenfalls beendet. Zum Schluss wird 
   # noch die Funktion exit() aufgerufen die die Motoren stoppt.
   if(char == "x"):
      HBridge.setMotor(0)
      HBridge.exit()
      print("Program Ended")
      break
   
   # Die Variable char wird pro Schleifendurchlauf geleert. 
   # Das ist notwendig um weitere Eingaben sauber zu übernehmen.
   char = ""
   
# Ende des Programmes
