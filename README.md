#slowglass
Python application simulating slowglass.

Slowglass captures still frames from a webcam at one framerate and displays them at a lower framerate creating a "window" into the past.  

##About
###Inspiration
Slowglass was inspired by the short story [Light of Other Days](https://en.wikipedia.org/wiki/Light_of_Other_Days) by Bob Shaw.

##Usage
run slowglass

    python slowglass.py
    

##Configuration
There is currently no configuration for slowglass.  Framerate and resolution are hardcoded into the code in player.py and capture.py.

##Prerequisites
Slowglass is written in python and uses the [simpleCV library](http://simplecv.org/).  
Slowglass has only been tested on OSX using the built in iSight camera
