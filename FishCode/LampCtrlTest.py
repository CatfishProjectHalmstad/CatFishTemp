import RPi.GPIO as GPIO
import time

#function for maping the input value of 0-1   to the correct range
def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y

def LampChangeBrightness(val, pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    pi_pwm = GPIO.PWM(pin, 50)
    pi_pwm.start(mapFromTo(val, 0, 1, 5, 9))
    print (mapFromTo(val, 0, 1, 5, 9))
