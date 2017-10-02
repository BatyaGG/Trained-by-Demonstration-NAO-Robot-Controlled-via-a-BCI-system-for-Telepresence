from time import sleep
import bufhelp
import FieldTrip
from NAO import NAO
import warnings
warnings.filterwarnings('ignore')

# Configuring NAO robot IP and its port and initializing NAO object
robotIP = "192.168.10.101"
robotPort = 9559
Nao = NAO(robotIP, robotPort)
for i in range(1):
    Nao.trainTask()

# Buffer interfacing functions
def sendEvent(event_type, event_value=1, offset=0):
    e = FieldTrip.Event()
    e.type = event_type
    e.value = event_value
    if offset > 0:
        sample, bla = ftc.poll() #TODO: replace this with a clock-sync based version
        e.sample = sample + offset + 1
    ftc.putEvents(e)

hostname='localhost'
port=1972
(ftc,hdr) = bufhelp.connect(hostname,port)
# Wait until the buffer connects correctly and returns a valid header

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

def processBufferEvents():
    events = bufhelp.buffer_newevents()
    for evt in events:
        print(str(evt.sample) + ": " + str(evt))
        # stimulus.prediction
        if evt.type == 'keyboard':
            if evt.value == '@FWRD':
                Nao.moveForward(50)
            elif evt.value == '@TRNL':
                Nao.turnLeft(90)
            elif evt.value == '@TRHT':
                Nao.turnRight(90)
            elif evt.value == '@LEFT':
                Nao.moveLeft(90)
            elif evt.value == '@RGHT':
                Nao.moveRight(90)
            elif evt.value == '@BACK':
                Nao.moveBackward(50)
            elif evt.value == '#HELLO':
                Nao.sayHello()
            elif evt.value == '#GBYE':
                Nao.sayBye()
            elif evt.value == '#HWRU':
                Nao.sayHRU()
            elif evt.value == '#FINE':
                Nao.sayFine()
            elif evt.value == '0':
                Nao.performTask(0)
            elif evt.value == '*CLAP':
                Nao.performTask(1)
            elif evt.value == '*SHAKE':
                Nao.performTask(2)

while True:
    processBufferEvents()