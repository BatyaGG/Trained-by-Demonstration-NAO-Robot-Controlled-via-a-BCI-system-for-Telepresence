from naoqi import ALProxy
import time
import numpy as np
class NAO:
    def __init__(self, robotIP, robotPort):
        # self.motionProxy = ALProxy("ALMotion", robotIP, robotPort)
        self.numberOfStates = 5

    def moveForward(self, distance):
        self.motionProxy.setWalkTargetVelocity(1, 0, 0, 0)
        time.sleep(4.5)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def turnLeft(self, angle):
        self.motionProxy.setWalkTargetVelocity(0, 0, 0.5, 0)
        time.sleep(angle / 15)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def turnRight(self, angle):
        self.motionProxy.setWalkTargetVelocity(0, 0, -0.5, 0)
        time.sleep(angle / 15)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def trainTask(self):
        # self.motionProxy.setStiffnesses(
        #     ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand'], 0.0)
        Data = []
        while True:
            raw_input('Press Enter key to start')
#             process

if __name__ == '__main__':
    NAO = NAO('asd', 123)
    NAO.trainTask()
    asd = raw_input('finished')
