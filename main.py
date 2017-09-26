from time import sleep
import bufhelp
import FieldTrip
from NAO import NAO
# Configuring NAO robot IP and its port and initializing NAO object
robotIP = "192.168.10.101"
robotPort = 9559
Nao = NAO(robotIP, robotPort)

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
        if evt.type == 'keyboard':
            if evt.value == 'q':
                Nao.moveForward(150)
            elif evt.value == 'w':
                Nao.turnLeft(90)
            elif evt.value == 'e':
                Nao.turnRight(90)
            elif evt.value == '0':
                print 'task'

while True:
    processBufferEvents()