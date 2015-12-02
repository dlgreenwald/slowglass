from SimpleCV import Image, Camera
from datetime import datetime
import time
from glob import glob


def Run(cmdPipe):
    steadyStateFPS = 10
    desiredBuffer = 60*60 #1 minute * 60 seconds
    numberOfFrames = steadyStateFPS*desiredBuffer;



    cam = Camera(0, {"width": 640, "height": 480})

    i = 10
    sleepTime = 0
    while True:
        # check command
        if cmdPipe.poll():
            cmd = cmdPipe.recv()
            if cmd=='shutdown':
                print('capture', 0, "Shutting down.")
                break

        filelist = glob("images/*.jpg")
        if len(filelist)<numberOfFrames:
            sleepTime = (1.0/steadyStateFPS)-.01
            print("capture", 0, "number of frames in buffer="+str(len(filelist))+" desired="+str(numberOfFrames)+" setting sleeptime to "+str(sleepTime))
        else:
            sleepTime = 1.0/steadyStateFPS
            print("capture", 0, "number of frames in buffer="+str(len(filelist))+" desired="+str(numberOfFrames)+" setting sleeptime to "+str(sleepTime))
        for index in range(100):
            ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            cam.getImage().save("images/slowglass."+ ts + ".jpg")
            time.sleep(sleepTime)
