#from wand.image import Image
from SimpleCV import Image
from SimpleCV import Display
from glob import glob
import os
import time

steadyStateFPS = 10
desiredBuffer = 1*60 #1 minute * 60 seconds
numberOfFrames = steadyStateFPS*desiredBuffer;

disp = Display()

filelist = []
frameCounter = 101
sleepTime = .1

while disp.isNotDone():
    if frameCounter > 100:
        frameCounter = 0
        filelist = glob("images/*.jpg")
        if len(filelist)<numberOfFrames:
            sleepTime = .1
            print "number of frames in buffer="+str(len(filelist))+" desired="+str(numberOfFrames)+" setting sleeptime to .1"
        else:
            sleepTime = .09
            print "number of frames in buffer="+str(len(filelist))+" desired="+str(numberOfFrames)+" setting sleeptime to .09"


    filename = filelist.pop(0)
    img = Image(filename)
    img.save(disp)
    os.remove(filename)
    frameCounter = frameCounter+1
    time.sleep(sleepTime)
