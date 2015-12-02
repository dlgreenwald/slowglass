
import sys, time
from os import sep
import socket
from multiprocessing import Process, Pipe
from multiprocessing.managers import BaseManager
import signal, errno
import shutil
import os

import capture, slowglass

procs = {}
pipes = {}
running = False

def startup():
    global procs
    global pipes
    global running

    #cleanup in case of bad shutdown
    shutil.rmtree('images', ignore_errors=True)
    os.mkdir("images")

    running = True

    # init capture
    master, slave = Pipe()  # endpoint [0]-PlexConnect, [1]-DNSServer
    proc = Process(target=capture.Run, args=[slave])
    proc.start()

    time.sleep(0.1)
    if proc.is_alive():
        procs['capture'] = proc
        pipes['capture'] = master
    else:
        print('Slowglass', 0, "capture not alive. Shutting down.")
        running = False

    time.sleep(2)
    # init player
    if running:
        master, slave = Pipe()  # endpoint [0]-PlexConnect, [1]-WebServer
        proc = Process(target=player.Run, args=[slave])
        proc.start()

        time.sleep(0.1)
        if proc.is_alive():
            procs['player'] = proc
            pipes['player'] = master
        else:
            dprint('Slowglass', 0, "player not alive. Shutting down.")
            running = False

    # not started successful - clean up
    if not running:
        cmdShutdown()
        shutdown

def shutdown():
    for slave in procs:
        procs[slave].join()
    shutil.rmtree('images')
    print('Slowglass', 0, "shutdown")

def cmdShutdown():
    global running
    running = False
    # send shutdown to all pipes
    for slave in pipes:
        pipes[slave].send('shutdown')
    print('Slowglass', 0, "Shutting down.")

def sighandler_shutdown(signum, frame):
    signal.signal(signal.SIGINT, signal.SIG_IGN)  # we heard you!
    cmdShutdown()

if __name__=="__main__":
    signal.signal(signal.SIGINT, sighandler_shutdown)
    signal.signal(signal.SIGTERM, sighandler_shutdown)

    print('Slowglass', 0, "***")
    print('Slowglass', 0, "Slowglass")
    print('Slowglass', 0, "Press CTRL-C to shut down.")
    print('Slowglass', 0, "***")

    running = startup()

    while running:
        running = run()

    shutdown()
