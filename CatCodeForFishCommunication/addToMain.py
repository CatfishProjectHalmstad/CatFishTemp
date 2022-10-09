
import threading
import time
import subprocess

#Importing scripts
import receiveData
import receiveimg
import sendData
#If the program crashes or is unexpectedly closed the ports for reciving data
#Will not be available
#By importing killPortUsage it makes sure the ports are available
import killPortUsage

def ReceiveIMG():
    while 1:
        time.sleep(1)
        receiveimg.receive()


def ReceiveData():
    while 1:
        time.sleep(1)
        receiveData.receiveData()

def SendData():
    while 1:
        time.sleep(0.5)
        sendData.sendD()




receiveImgThread = threading.Thread(target=ReceiveIMG)
receiveImgThread.start()

receiveDataThread = threading.Thread(target=ReceiveData)
receiveDataThread.start()

SendDataThread = threading.Thread(target=SendData)
SendDataThread.start()



"""
def ReceiveIMG():
    receiveImgThread = threading.Thread(target=self.ReceiveIMG)
    
    receiveimg.receive()
    receiveImgThread.start()
    receiveImgThread.start()


def temp():
    receiveImgThread = threading.Thread(target=self.temp)
    print("eello")
    receiveImgThread.start()



if __name__ == "__main__":
    print("Trying")
    temp()
    ReceiveIMG()
"""

while 1:
    #Restart the receive threads as they lose connection and crash some times
    if receiveImgThread.is_alive() == False:
        receiveImgThread = threading.Thread(target=ReceiveIMG)
        receiveImgThread.start()

    if receiveDataThread.is_alive() == False:
        receiveDataThread = threading.Thread(target=ReceiveData)
        receiveDataThread.start()

    if SendDataThread.is_alive() == False:
        SendDataThread = threading.Thread(target=SendData)
        SendDataThread.start()




    time.sleep(1)
    print("ee")