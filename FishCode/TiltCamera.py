import RPi.GPIO as GPIO
import time

#33 pin for camera tilt pwm

#function for maping the input value of 0-1   to the correct range for diffrent pwm signals
def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y

##
def cameraInit(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(pin,50)
    servo.start(0.65)
    

#value 4 to 10
def rotate(tilt, pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    servo = GPIO.PWM(33,50)
    servo.start(mapFromTo(tilt, 0, 1, 4, 10))
    time.sleep(0.002)
    servo.stop()
    
    

