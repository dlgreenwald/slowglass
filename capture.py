from SimpleCV import Image, Camera
from datetime import datetime
import time
from glob import glob

steadyStateFPS = 10
desiredBuffer = 1*60 #1 minute * 60 seconds
numberOfFrames = steadyStateFPS*desiredBuffer;



cam = Camera()

i = 10
sleepTime = 0
while True:
    filelist = glob("images/*.jpg")
    if len(filelist)<numberOfFrames:
        sleepTime = .09
        print "number of frames in buffer="+str(len(filelist))+" desired="+str(numberOfFrames)+" setting sleeptime to .09"
    else:
        sleepTime = .1
        print "number of frames in buffer="+str(len(filelist))+" desired="+str(numberOfFrames)+" setting sleeptime to .1"
    for index in range(100):
        ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        cam.getImage().save("images/slowglass."+ ts + ".jpg")
        time.sleep(sleepTime)
