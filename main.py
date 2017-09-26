#!/usr/bin/env python3
## CONFIGURABLE VARIABLES
# Path of the folder containing the buffer client
bufferpath = "../../dataAcq/buffer/python"
sigProcPath = "../signalProc"

# Connection options of fieldtrip, hostname and port of the computer running the fieldtrip buffer.
hostname='localhost'
port=1972

#Set to True if the program has to run in fullscreen mode.
fullscreen = False #True

#The default number of epochs.
number_of_epochs = 14

#The number of stimuli to play.
number_of_stimuli = 6

#The number of times to repeat each stimulus in a training sequence
number_of_repeats = 3

# set to true for keyboard control of the experimental progression
keyboard = True

sequence_duration         = 15
testing_sequence_duration = 120
inter_stimulus_interval   = .3
target_to_target_interval = 1
baseline_duration         = 3
target_duration           = 2
inter_trial_duration      = 3
sequences_for_break       = 3

# flag to indicate we should end training/testing early
endSeq=False

## END OF CONFIGURABLE VARIABLES
import numpy as np
import bufhelp
import pygame, sys
from naoqi import ALProxy
from pygame.locals import *
from random import shuffle, randint, random
from time import sleep, time

import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),bufferpath))
import FieldTrip
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),sigProcPath))
import stimseq

robotIP = "192.168.10.102"
motionProxy = ALProxy("ALMotion", robotIP, 9559)

def moveForward(distance):
    motionProxy.setWalkTargetVelocity(1, 0, 0, 0)
    sleep(4.5)
    motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

def turnLeft(angle):
    motionProxy.setWalkTargetVelocity(0, 0, 0.5, 0)
    sleep(angle/15)
    motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

def turnRight(angle):
    motionProxy.setWalkTargetVelocity(0, 0, -0.5, 0)
    sleep(angle/15)
    motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

# Buffer interfacing functions
def sendEvent(event_type, event_value=1, offset=0):
    e = FieldTrip.Event()
    e.type = event_type
    e.value = event_value
    if offset > 0:
        sample, bla = ftc.poll() #TODO: replace this with a clock-sync based version
        e.sample = sample + offset + 1
    ftc.putEvents(e)

# Connecting to Buffer
timeout = 5000
# ftc = FieldTrip.Client()
(ftc,hdr) = bufhelp.connect(hostname,port)
# Wait until the buffer connects correctly and returns a valid header
hdr = None;
while hdr is None:
    print(('Trying to connect to buffer on %s:%i ...' % (hostname, port)))
    try:
        ftc.connect(hostname, port)
        print('\nConnected - trying to read header...')
        hdr = ftc.getHeader()
    except IOError:
        pass

    if hdr is None:
        print('Invalid Header... waiting')
        sleep(1)
    else:
        print(hdr)
        print((hdr.labels))
fSample = hdr.fSample

def processBufferEvents():
    global running
    events = bufhelp.buffer_newevents()

    for evt in events:
        print(str(evt.sample) + ": " + str(evt))
        if evt.type == 'keyboard':
            if evt.value == 'q':
                moveForward(150)
            elif evt.value == 'w':
                turnLeft(90)
            elif evt.value == 'e':
                turnRight(90)
            elif evt.value == '0':
                print 'task'



sendEvent('startPhase.cmd','eegviewer')
while True:
    a = ftc.getData()
    processBufferEvents()