from __future__ import division
import time

from pyPS4Controller.controller import Controller
import Adafruit_PCA9685


#Variablen
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

#Räder gerade stellen
pwm.set_pwm(0, 0, 225)

#rechts lenken
while True:
  pwm.set_pwm(0, 0, right_servo)
  time.sleep(0.001)
