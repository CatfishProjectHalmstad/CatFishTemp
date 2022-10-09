#This is the main python script run this to run the program
#GPIO MODE BOARD!!!

#Static eth0 fish ip   192.168.0.11
#Static eth0 cat ip    192.168.3.10
#Port for data going to cat 5001
#Port for data going to fish 5002

#In the data file please send only a maximum of 10 numbers per line
import RPi.GPIO as GPIO
import time
import os
import threading

from cv2 import CAP_PROP_XI_IMAGE_DATA_BIT_DEPTH

#tiltcamera TiltCamera.rotate(0-1, cameratiltPin)
#LampChangeBrightness(0-1)
#leak sensor pin turns high on leak
#pins of corrensponding functions
lampPin = 12
leaksensorPin = 7
cameratiltPin = 33

outputDataFile = "dataout.txt"
inputDataFile = "datain.txt"


OldCameraValue = 0
OldLampValue = 0


#setup gpios
GPIO.setmode(GPIO.BOARD)
GPIO.setup(lampPin, GPIO.OUT)
GPIO.setup(leaksensorPin, GPIO.IN)

#init lamp pwm
pi_pwm = GPIO.PWM(lampPin, 50)
pi_pwm.start(4)

#From cat
timeAtLastPackageRecived = 0





#Import other scripts
import TiltCamera
from sendimg import sendIMG
from SendData import sendD
import receiveData

#kills any maybe existing usage of the port used for reciving data from the cat
import killPortUsage


#function for taking the images
def takeImgAndSendData():

    #The usb camera will be busy if the script is turned off 
    #These two lines dissable the usb ports and then re enables them 
    #This also restarts the ethernet which might cause problems later
    os.system("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind")
    os.system("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind")
    
    #wait for the usb to start
    time.sleep(1)
    #Unessesary code as we are no longer finding the camera by /dev/video but by id

    """
    #Keep track of which port the camera is bound to
    devid = 0
    

    #This code tests all the /dev/video for the correct one
    testusbdev1 = "sudo v4l2-ctl --device=/dev/video"
    testusbdev2 = " --all"
    
    while 1:
        com = testusbdev1 + str(devid) + testusbdev2
        out = os.system(com) 
        print(out)
        #Breaks out of the while loop when the correct dev is found
        if out == 0:
            break
        devid = devid + 1
        if devid > 9 and devid < 17:
            devid = 17
        print("No Camera on dev/video" + str(devid))
    """
    while 1:
        """
        #Takes the spliced command for taking an image and inserts the correct dev/video nummber
        p1 = "fswebcam"
        #to make changes to the video add arguments to p2
        #To see what arguments can be added write fswebcam --help in the console
        p2 = " -r 1280x720 --no-banner -q fishimg.jpg"
        dev = " --device /dev/video"
        command = p1 + dev + str(devid) + p2
        """
        #Needs to be changed to use another webcam
        #ls /dev/v41/by-id/ -1h    to find the id of the camera
        camid = "usb-H264_USB_Camera_H264_USB_Camera_2020032801-video-index0"
        command = "fswebcam --device /dev/v4l/by-id/"+ camid +" -r 1280x720 --no-banner -q fishimg.jpg"
        os.system(command)

        #send the photo
        sendIMG()
        sendD()




#Starts a new thread which continussly saves the webcam Img sends it
#And sends the other Values 
SendDataThread = threading.Thread(target=takeImgAndSendData)
SendDataThread.start()

"""
def receive():
    while 1:
        time.sleep(0.5)
        receiveData.receiveData()

#Start receive data thread
ReceiveThread = threading.Thread(target=receive)
ReceiveThread.start()
"""


#Function for remaping values to specific ranges
def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y


#change the brightness of the lamps, from 0 to 1
def LampChangeBrightness(val):
    pi_pwm.ChangeDutyCycle(mapFromTo(val, 0, 1, 5, 9))


#write data to the file which will be sent to the cat
def WriteDataToFile():
    datafile = open(outputDataFile, "w")
    datafile.write(str(GPIO.input(leaksensorPin)))
    #Need to add the sensory data here
    datafile.close()



#Read the data file which was recived form the cat
def ReadInputs():
    receiveData.receiveData()
    data = open(inputDataFile, "r")
    cameraAngle = float(data.readline())
    lampBrightness = float(data.readline())
    data.close()
    return cameraAngle, lampBrightness


#Reads the information from the cat and updates the camera angle and lamps acordingly
#This function also runs the code for everything involving getting data from the cat!
def GetAndUpdateValues():
    while 1:
        camera, lamp = ReadInputs()
        global OldLampValue, OldCameraValue
        if (camera != OldCameraValue):
            OldCameraValue = camera
            TiltCamera.rotate(camera, cameratiltPin)
        
        if(lamp != OldLampValue):
            OldLampValue = lamp
            LampChangeBrightness(lamp)
        print("Updated")
        time.sleep(1)


ReceiveDataThread = threading.Thread(target=GetAndUpdateValues)
ReceiveDataThread.start()

WriteDataToFile()



i = 0
while 1:
    #Sometimes the network script fails this restarts the thread in case it is terminated
    print(SendDataThread.is_alive())
    if SendDataThread.is_alive() == False:
        SendDataThread = threading.Thread(target=takeImgAndSendData)
        SendDataThread.start()
        print("restarting Send Data Thread")

    print(ReceiveDataThread.is_alive())

    if ReceiveDataThread.is_alive() == False:
        ReceiveDataThread = threading.Thread(target=GetAndUpdateValues)
        ReceiveDataThread.start()
        print("restarting Receive Data Thread")


    print("loop")
   
    time.sleep(1)







GPIO.cleanup()

