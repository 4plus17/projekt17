#!/usr/bin/env python
# Blockzeit: 748409
# Version:   1.0
# Dieses Programm ist das sogenannte Steuerprogramm fuer den Motor
# ueber die Konsole und Tastatur vom PC aus.


# Es werden verschiedene Python Klassen importiert deren Funktionen
# im Programm benoetigt werden fuer die Programmverarbeitung.
import sys, tty, termios, os, readchar

# Das Programm BTS7960HBridgePCA9685.py wird als Modul geladen. Es stellt
# die Funktionen fuer die Steuerung der H-Bruecke zur Verfuegung.
# definierte Funktionen sind:
# "setMode(mode)" mode ist aus {reverse, forward}
# "setSpeed(power)" power ist aus {-1,1}
# "exit()" Pins aus, PWM aus
import BTS7960HBridgePCA9685 as HBridge

# Variablen Definition der Geschwindigkeit des Motors.
speed = 0

# Das Menue fuer den Anwender wenn er das Programm ausfuehrt.
# Das Menue erklaert mit welchen Tasten das Auto gesteuert wird.
print("w/s: beschleunigen")
print("a/d: lenken")
print("q: stoppt die Motoren")
print("x: Programm beenden")

# Die Funktion getch() nimmt die Tastatureingabe des Anwenders
# entgegen. Die gedrueckten Buchstaben werden eingelesen. Sie werden
# benoetigt um die Richtung und Geschwindigkeit festlegen zu koennen.
def getch():
   ch = readchar.readchar()
   return ch

# Die Funktion printscreen() gibt immer das aktuelle Menue aus
# sowie die Geschwindigkeit des Motores wenn es aufgerufen wird.
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
   print ("Geschwindigkeit Motor:  ", speed)

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

   # Der Motor dreht vorwaerts wenn der Anwender die Taste "w" drueckt.
   if(char == "w"):
      # der Motor beschleunigt in Schritten von 10%
      # mit jedem Tastendruck des Buchstaben "w" bis maximal
      # 100%. Dann faehrt es maximal schnell vorwaerts.
      speed = speed + 0.1

      if speed > 1:
         speed = 1
      # Dem Programm BTS7960HBridgePCA9685.py welches zu beginn
      # importiert wurde wird die Geschwindigkeit fuer den Motor uebergeben.
      HBridge.setSpeed(speed)
      printscreen()

   # Das Roboter-Auto faehrt rueckwaerts wenn die Taste "s"
   # gedrueckt wird.
   if(char == "s"):
      # das Roboter-Auto bremst in Schritten von 10%
      # mit jedem Tastendruck des Buchstaben "s" bis maximal
      # -100%. Dann faehrt es maximal schnell rueckwaerts.
      speed = speed - 0.1

      if speed < -1:
         speed = -1

      # Dem Programm BTS7960HBridgePCA9685.py welches zu beginn
      # importiert wurde wird die Geschwindigkeit fuer den Motor uebergeben.
      HBridge.setSpeed(speed)
      printscreen()

    # mit dem druecken der Taste "q" wird der Motor angehalten
   if(char == "q"):
      speed = 0
      HBridge.setSpeed(0)
      printscreen()

   # Mit der Taste "x" wird die Endlosschleife beendet
   # und das Programm wird ebenfalls beendet. Zum Schluss wird
   # noch die Funktion exit() aufgerufen die den Motor stoppt.
   if(char == "x"):
      HBridge.setSpeed(0)
      HBridge.exit()
      print("Program Ended")
      break

   # Die Variable char wird pro Schleifendurchlauf geleert.
   # Das ist notwendig um weitere Eingaben sauber zu übernehmen.
   char = ""

# Ende des Programmes
