from naoqi import ALProxy
import time
import numpy as np
import thread
from DTW import DTW
from GMM_GMR import GMM_GMR
from matplotlib import pyplot as plt
class NAO:

    def __init__(self, robotIP, robotPort):
        self.motionProxy = ALProxy("ALMotion", robotIP, robotPort)
        self.numberOfStates = 5
        self.trainedTasks = []
        self.stopperBool = True

    def moveForward(self, distance):
        self.motionProxy.setWalkTargetVelocity(1, 0, 0, 0)
        time.sleep(distance / 10)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def moveBackward(self, distance):
        self.motionProxy.setWalkTargetVelocity(-1, 0, 0, 0)
        time.sleep(distance / 10)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def moveLeft(self, distance):
        self.motionProxy.setWalkTargetVelocity(0, 1, 0, 0)
        time.sleep(distance / 10)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def moveRight(self, distance):
        self.motionProxy.setWalkTargetVelocity(0, -1, 0, 0)
        time.sleep(distance / 10)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def turnLeft(self, angle):
        self.motionProxy.setWalkTargetVelocity(0, 0, 0.5, 0)
        time.sleep(angle / 15)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def turnRight(self, angle):
        self.motionProxy.setWalkTargetVelocity(0, 0, -0.5, 0)
        time.sleep(angle / 15)
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

    def performTask(self, index):
        

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
                timeArray = np.hstack((timeArray, np.array([[timeArray[0, -1] + elapsed]])))
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

        self.motionProxy.setStiffnesses(
            ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand',
                'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand'], 1.0)

        inputMat = DataLeft[0][0, :]
        DataLeft = DTW(DataLeft)
        DataRight = DTW(DataRight)
        leftGMR = GMM_GMR(self.numberOfStates)
        rightGMR = GMM_GMR(self.numberOfStates)
        leftGMR.fit(DataLeft)
        rightGMR.fit(DataRight)
        leftGMR.predict(inputMat)
        rightGMR.predict(inputMat)

        self.trainedTasks.append((leftGMR.getPredictedMatrix(), rightGMR.getPredictedMatrix()))

        # fig = plt.figure()
        # ax1 = fig.add_subplot(121)
        # plt.title('Left Hand x-axis trajectory')
        # leftGMR.plot(ax=ax1, plotType="Clusters")
        # leftGMR.plot(ax=ax1, plotType="Regression")
        # ax2 = fig.add_subplot(122)
        # plt.title('Right Hand x-axis trajectory')
        # rightGMR.plot(ax=ax2, plotType="Clusters")
        # rightGMR.plot(ax=ax2, plotType="Regression")
        # plt.show()

if __name__ == '__main__':
    NAO = NAO('192.168.10.101', 9559)
    NAO.trainTask()