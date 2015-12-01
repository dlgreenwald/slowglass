from wand.image import Image
import os
import tempfile
from subprocess import Popen, PIPE


filelist = ['new.jpg']

fps, duration = 24, 100
p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-s', '300x300', '-vcodec', 'mjpeg', '-i', '-', '-vcodec', 'libx264', '-pix_fmt',  'yuv444p', 'video.mp4'], stdin=PIPE, bufsize=0)
for f in filelist:
    bg = Image(width=300, height=300)
    bg.depth = 8

    i = open(f, "r").read()
    img = Image(blob=i)
    bg.composite(img, left=0, top=0)

    blob = bg.make_blob("jpeg")
    out = open('new.jpg', "w")
    p.stdin.write(blob)
    bg.close()
p.stdin.close()
p.wait()
