from naoqi import ALProxy
import time
import numpy as np
import thread
class NAO:
    def __init__(self, robotIP, robotPort):
        self.motionProxy = ALProxy("ALMotion", robotIP, robotPort)
        self.numberOfStates = 5
        self.stopperBool = True

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

        def stopper(self):
            raw_input('Press Enter to stop demonstration.')
            self.stopperBool = False

        def recordData():
            dataLeft = np.zeros((6,0))
            dataRight = np.zeros((6,0))
            timeArray = np.array([[0.1]])
            thread.start_new_thread(stopper, (self, ))
            while self.stopperBool:
                startTime = time.time()
                resultLeft = self.motionProxy.getPosition('LArm', 0, True)
                resultLeft = np.reshape(resultLeft, (6,1))
                resultRight = self.motionProxy.getPosition('RArm', 0, True)
                resultRight = np.reshape(resultRight, (6,1))
                dataLeft = np.hstack((dataLeft, resultLeft))
                dataRight = np.hstack((dataRight, resultRight))
                elapsed = time.time() - startTime
                timeArray = np.hstack((timeArray, np.array([[elapsed]])))
            timeArray = timeArray[:,:(timeArray.size - 1)]
            self.stopperBool = True
            return np.vstack((timeArray, dataLeft)), np.vstack((timeArray, dataRight))

        self.motionProxy.setStiffnesses(
            ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand',
                'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand'], 0.0)

        DataLeft = []
        DataRight = []
        while True:
            startDemo = raw_input('Do you want to start new demonstration? (Y/N): ')
            if startDemo == 'Y':
                left, right = recordData()
                DataLeft.append(left)
                DataRight.append(right)
            elif startDemo == 'N':
                print 'Data recording is finished.'
                break
            else:
                print 'Incorrect input given.'

        

if __name__ == '__main__':
    NAO = NAO('192.168.10.101', 9559)
    NAO.trainTask()
