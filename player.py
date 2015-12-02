from SimpleCV import Image, Display
from glob import glob
import os
import time
from datetime import datetime
import re



def Run(cmdPipe):
    steadyStateFPS = 10
    desiredBuffer = 60*60 #1 minute * 60 seconds
    numberOfFrames = steadyStateFPS*desiredBuffer;
    fmt = '%Y-%m-%d %H:%M:%S'

    disp = Display()

    filelist = []
    frameCounter = 101
    sleepTime = .1

    while disp.isNotDone():
        # check command
        if cmdPipe.poll():
            cmd = cmdPipe.recv()
            if cmd=='shutdown':
                break

        if frameCounter > 100 or len(filelist) == 0:
            frameCounter = 0
            filelist = glob("images/*.jpg")
            if len(filelist)>numberOfFrames:
                sleepTime = 1.0/steadyStateFPS
                print("player", 0, "number of frames in buffer="+str(len(filelist))+" desired="+str(numberOfFrames)+" setting sleeptime to "+str(sleepTime))
            else:
                sleepTime = (1.0/steadyStateFPS)+.01
                print("player", 0, "number of frames in buffer="+str(len(filelist))+" desired="+str(numberOfFrames)+" setting sleeptime to "+str(sleepTime))


        filename = filelist.pop(0)
        img = Image(filename)
        matchObj = re.search(r'[0-9- :]+', filename)

        d1_ts = time.mktime(datetime.strptime(matchObj.group(), fmt).timetuple())
        d2_ts = time.mktime(datetime.utcnow().timetuple())
        offset = int(d1_ts-d2_ts)/60
        img.drawText(str(offset),  x=600, y=470)
        img.save(disp)
        os.remove(filename)
        frameCounter = frameCounter+1
        time.sleep(sleepTime)
