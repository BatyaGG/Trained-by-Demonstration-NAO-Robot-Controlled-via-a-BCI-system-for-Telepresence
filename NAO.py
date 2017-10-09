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
        self.sayProxy = ALProxy("ALTextToSpeech", robotIP, robotPort)
        self.numberOfStates = 15
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

    def sayHello(self):
        self.sayProxy.say("Hello!")

    def sayBye(self):
        self.sayProxy.say("Good bye!")

    def sayHRU(self):
        self.sayProxy.say("How are you?")

    def sayFine(self):
        self.sayProxy.say("I am fine, thanks!")

    def performTask(self, index):

        effector = ['LArm', 'RArm']
        space = 0
        axisMask = [63, 63]
        isAbsolute = True
        currentTask = self.trainedTasks[index]
        pathList = [currentTask[0][1:, :].T.tolist(), currentTask[1][1:, :].T.tolist()]
        timeList = [currentTask[0][0, :].tolist(), currentTask[1][0, :].tolist()]
        self.motionProxy.positionInterpolations(effector, space, pathList, axisMask, timeList, isAbsolute)

    def trainTask(self):

        def stopper(self):
            raw_input('Press Enter to stop demonstration.')
            self.stopperBool = False

        def recordData(self):
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
                elapsed = time.time() - startTime + 0.005
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
                left, right = recordData(self)
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

        fig = plt.figure()
        ax1 = fig.add_subplot(231)
        plt.title('Left Hand x-axis trajectory')
        leftGMR.plot(ax=ax1, plotType="Data")
        leftGMR.plot(ax=ax1, plotType="Regression")
        ax2 = fig.add_subplot(232)
        plt.title('Left Hand y-axis trajectory')
        leftGMR.plot(yAxis = 2, ax=ax2, plotType="Data")
        leftGMR.plot(yAxis = 2, ax=ax2, plotType="Regression")
        ax3 = fig.add_subplot(233)
        plt.title('Left Hand z-axis trajectory')
        leftGMR.plot(yAxis = 3, ax=ax3, plotType="Data")
        leftGMR.plot(yAxis = 3, ax=ax3, plotType="Regression")
        ax4 = fig.add_subplot(234)
        plt.title('Left Hand x-axis trajectory')
        leftGMR.plot(yAxis=4, ax=ax4, plotType="Data")
        leftGMR.plot(yAxis=4, ax=ax4, plotType="Regression")
        ax5 = fig.add_subplot(235)
        plt.title('Left Hand y-axis orientation')
        leftGMR.plot(yAxis=5, ax=ax5, plotType="Data")
        leftGMR.plot(yAxis=5, ax=ax5, plotType="Regression")
        ax6 = fig.add_subplot(236)
        plt.title('Left Hand z-axis trajectory')
        leftGMR.plot(yAxis=6, ax=ax6, plotType="Data")
        leftGMR.plot(yAxis=6, ax=ax6, plotType="Regression")

        fig = plt.figure()
        ax1 = fig.add_subplot(231)
        plt.title('Right Hand x-axis trajectory')
        rightGMR.plot(ax=ax1, plotType="Data")
        rightGMR.plot(ax=ax1, plotType="Regression")
        ax2 = fig.add_subplot(232)
        plt.title('Right Hand y-axis trajectory')
        rightGMR.plot(yAxis=2, ax=ax2, plotType="Data")
        rightGMR.plot(yAxis=2, ax=ax2, plotType="Regression")
        ax3 = fig.add_subplot(233)
        plt.title('Right Hand z-axis trajectory')
        rightGMR.plot(yAxis=3, ax=ax3, plotType="Data")
        rightGMR.plot(yAxis=3, ax=ax3, plotType="Regression")
        ax4 = fig.add_subplot(234)
        plt.title('Right Hand x-axis trajectory')
        rightGMR.plot(yAxis=4, ax=ax4, plotType="Data")
        rightGMR.plot(yAxis=4, ax=ax4, plotType="Regression")
        ax5 = fig.add_subplot(235)
        plt.title('Right Hand y-axis orientation')
        rightGMR.plot(yAxis=5, ax=ax5, plotType="Data")
        rightGMR.plot(yAxis=5, ax=ax5, plotType="Regression")
        ax6 = fig.add_subplot(236)
        plt.title('Right Hand z-axis trajectory')
        rightGMR.plot(yAxis=6, ax=ax6, plotType="Data")
        rightGMR.plot(yAxis=6, ax=ax6, plotType="Regression")
        plt.show()
        self.trainedTasks.append((leftGMR.getPredictedMatrix(), rightGMR.getPredictedMatrix()))