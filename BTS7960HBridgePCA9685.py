#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20170616
# Version:   1.0 Alpha
# Homepage:   http://custom-build-robots.com

# Dieses Programm wurde fuer die Ansteuerung der linken und rechten
# Motoren des Roboter-Autos BigRob entwickelt. Das Programm erwartet,
# dass zwei BTS7960  H-Bruecken als Motor Treiber eingesetzt
# werden. Das PWM Signal wird von einem PCA9685 Servo Kontroller
# erzeugt für die Regelung der Geschwindigkeit der Motoren.

# Dieses Programm muss von einem uebergeordneten Programm z. B.
# RobotControl.py aufgerufen werden, dass die Steuerung des  
# Programmes BTS7960HBridgePCA9685.py übernimmt.

# Es wird die Klasse RPi.GPIO importiert, die die Ansteuerung
# der GPIO Pins des Raspberry Pi ermoeglicht.
from __future__ import division
import RPi.GPIO as io
io.setmode(io.BCM)

import time

# Importiere die Adafruit PCA9685 Bibliothek
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
PCA9685_pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
#MA_pwm = 0  # Min pulse length out of 4096
#MB_pwm = 0  # Max pulse length out of 4096

# Eine Frequenz von 100hz, ist gut für die H-Bruecken.
# Sollen parallel zu dem BTS7960 noch Servo Motoren angesteuert
# werden, dann muss mit 60Hz gearbeitet werden.
PCA9685_pwm.set_pwm_freq(60)

# Die Variable duty_cycle gibt die maximale Einschaltdauer der 
# Motoren pro 100 Herts vor. Dier liegt zwischen 0 bis 4095.
# Für die Geschwindigkeit der Motoren beginnt die Einschaltdauer
# immer bei 0 und endet bei einem Wert ]0, 4095[.
duty_cycle = 4095

# Mit dem folgenden Aufruf werden eventuelle Warnungen die die 
# Klasse RPi.GPIO ausgibt deaktiviert.
io.setwarnings(False)

# Im folgenden Programmabschnitt wird die logische Verkabelung des 
# Raspberry Pi im Programm abgebildet. Dazu werden den vom Motor 
# Treiber bekannten Pins die GPIO Adressen des Raspberry Pi oder
# die des PCA9685 für das PWM Signal zugewiesen.

# --- ENDE KONFIGURATION GPIO Adressen ---

# Der Variable motor_in1_pin wird die Varibale IN1 zugeorndet. 
# Der Variable motor_in2_pin wird die Varibale IN2 zugeorndet. 
motor_in1_pin = 22
motor_in2_pin = 23
# Beide Variablen leftmotor_in1_pin und leftmotor_in2_pin werden als
# Ausgaenge "OUT" definiert. Mit den beiden Variablen wird die
# Drehrichtung der Motoren gesteuert.
io.setup(motor_in1_pin, io.OUT)
io.setup(motor_in2_pin, io.OUT)

# Die GPIO Pins des Raspberry Pi werden initial auf False gesetzt.
# So ist sichger gestellt, dass kein HIGH Signal anliegt und der 
# Motor Treiber nicht unbeabsichtigt aktiviert wird.

io.output(motor_in1_pin, True)
io.output(motor_in2_pin, True)

# Die Funktion setMotorMode(motor, mode) legt die Drehrichtung der 
# Motoren fest. Die Funktion verfügt über zwei Eingabevariablen.
# motor      -> diese Variable legt fest ob der linke oder rechte 
#              Motor ausgewaehlt wird.
# mode      -> diese Variable legt fest welcher Modus gewaehlt ist
# Beispiel:
# setMotorMode(leftmotor, forward)   Der linke Motor ist gewaehlt
#                                   und dreht vorwaerts .
# setMotorMode(rightmotor, reverse)   Der rechte Motor ist ausgewaehlt 
#                                   und dreht rueckwaerts.
# setMotorMode(rightmotor, stopp)   Der rechte Motor ist ausgewaehlt
#                                   der gestoppt wird.

def setMotorMode(mode):
	if mode == "reverse":
		io.output(motor_in1_pin, True)
		io.output(motor_in2_pin, False)
	elif  mode == "forward":
		io.output(motor_in1_pin, False)
		io.output(motor_in2_pin, True)
	else:
		io.output(motor_in1_pin, False)
		io.output(motor_in2_pin, False)

# Die Funktion setMotorLeft(power) setzt die Geschwindigkeit der 
# linken Motoren. Die Geschwindigkeit wird als Wert zwischen -1
# und 1 uebergeben. Bei einem negativen Wert sollen sich die Motoren 
# rueckwaerts drehen ansonsten vorwaerts. 
# Anschliessend werden aus den uebergebenen Werten die notwendigen 
# %-Werte fuer das PWM Signal berechnet.

# Beispiel:
# Die Geschwindigkeit kann mit +1 (max) und -1 (min) gesetzt werden.
# Das Beispielt erklaert wie die Geschwindigkeit berechnet wird.
# SetMotorLeft(0)     -> der linke Motor dreht mit 0% ist gestoppt
# SetMotorLeft(0.75)  -> der linke Motor dreht mit 75% vorwaerts
# SetMotorLeft(-0.5)  -> der linke Motor dreht mit 50% rueckwaerts
# SetMotorLeft(1)     -> der linke Motor dreht mit 100% vorwaerts
def setMotor(power):
   int(power)
   if power < 0:
      # Rueckwaertsmodus fuer den linken Motor
      pwm = -int(duty_cycle * power)
      if pwm > duty_cycle:
         pwm = duty_cycle
      PCA9685_pwm.set_pwm(0, 0, pwm)
      PCA9685_pwm.set_pwm(1, 0, 0)   
   elif power > 0:
      # Vorwaertsmodus fuer den linken Motor
      pwm = int(duty_cycle * power)
      if pwm > duty_cycle:
         pwm = duty_cycle
      PCA9685_pwm.set_pwm(0, 0, 0)
      PCA9685_pwm.set_pwm(1, 0, pwm)  	  
   else:
      # Stoppmodus fuer den linken Motor
      PCA9685_pwm.set_pwm(0, 0, 0)
      PCA9685_pwm.set_pwm(1, 0, 0)

	  
# Die Funktion exit() setzt die Ausgaenge die den Motor Treiber 
# steuern auf False. So befindet sich der Motor Treiber nach dem 
# Aufruf derFunktion in einem gesicherten Zustand und die Motoren 
# sind gestopped.
def exit():
   io.output(motor_in1_pin, False)
   io.output(motor_in2_pin, False)
   io.cleanup()
   # Hier wird das PWM Signal der vier Kanaele auf 0 gesetzt. 
   PCA9685_pwm.set_pwm(0, 0, 0)
   PCA9685_pwm.set_pwm(1, 0, 0)
# Ende des Programmes
