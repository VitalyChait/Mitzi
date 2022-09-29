#!/usr/bin/env python3
from subprocess import Popen


def findMotorPath(x=True, y=True, z=True, xPath=None, yPath=None, zPath=None):
    if x is False and y is False and z is False:
        return None, None, None

    motorOneFileName = "small_6600btmotorscript.sh"
    motorTwoFileName = "medium_6600btmotorscript.sh"
    motorThrFileName = "big_6600btmotorscript.sh"

    from os import getcwd
    from os.path import isdir, isfile
    if isdir(getcwd() + "/app/hardware/bashscripts/"):
        scriptDirPath = getcwd() + "/app/hardware/bashscripts/"
    else:
        scriptDirPath = "/home/orangepi/mitziProject/app/hardware/bashscripts/"

    if x:
        if xPath is not None:
            motorOne = xPath
        else:
            motorOne = scriptDirPath + motorOneFileName
        if not isfile(motorOne):
            print("ERROR FINDING MOTOR ONE SCRIPT")
            print(motorOne)
            exit()
    else:
        motorOne = None
    if y:
        if yPath is not None:
            motorTwo = yPath
        else:
            motorTwo = scriptDirPath + motorTwoFileName
        if not isfile(motorTwo):
            print("ERROR FINDING MOTOR TWO SCRIPT")
            print(motorTwo)
            exit()
    else:
        motorTwo = None
    if z:
        if zPath is not None:
            motorThr = zPath
        else:
            motorThr = scriptDirPath + motorThrFileName
        if not isfile(motorThr):
            print("ERROR FINDING MOTOR THREE SCRIPT")
            print(motorThr)
            exit()
    else:
        motorThr = None

    return motorOne, motorTwo, motorThr


class DummyMotorController:
    def __init__(self, x=True, y=True, z=True, xStepCount=50, yStepCount=50, zStepCount=200, xPath=None, yPath=None, zPath=None):
        motorOneFileName, motorTwoFileName, motorThreeFileName = findMotorPath(x=False, y=False, z=False, xPath=xPath, yPath=yPath, zPath=zPath)
        if x:
            self.xPos = 0
            self.xEnabled = True
            self.xStep = xStepCount
            self.motorOne = motorOneFileName
        if y:
            self.yPos = 0
            self.yEnabled = True
            self.yStep = yStepCount
            self.motorTwo = motorTwoFileName
        if z:
            self.zPos = 0
            self.zEnabled = True
            self.zStep = zStepCount
            self.motorThr = motorThreeFileName

        self.setupMotor()

    def setupMotor(self):
        print("Enabling Motors")

    def cleanupMotor(self):
        print("Closing Motors")

    def __del__(self):
        self.cleanupMotor()

    def getXPos(self):
        if self.xEnabled:
            return self.xPos
        return 0

    def getYPos(self):
        if self.yEnabled:
            return self.yPos
        return 0

    def getZPos(self):
        if self.zEnabled:
            return self.zPos
        return 0

    def getXStepCount(self):
        if self.xEnabled:
            return self.xStep
        return 0

    def getYStepCount(self):
        if self.yEnabled:
            return self.yStep
        return 0

    def getZStepCount(self):
        if self.zEnabled:
            return self.zStep
        return 0

    def xfw(self, step=1):
        self.xPos += step
        self.xPos = (self.xPos % self.xStep)

    def xbw(self, step=1):
        self.xPos += step
        self.xPos = (self.xPos % self.xStep)

    def yfw(self, step=1):
        self.yPos += step
        self.yPos = (self.yPos % self.yStep)

    def ybw(self, step=1):
        self.yPos += step
        self.yPos = (self.yPos % self.yStep)

    def zfw(self, step=1):
        self.zPos += step
        self.zPos = (self.zPos % self.zStep)

    def zbw(self, step=1):
        self.zPos += step
        self.zPos = (self.zPos % self.zStep)

    def fullX(self, loops=1):
        pass

    def fullY(self, loops=1):
        pass

    def fullZ(self, loops=1):
        pass


class MotorController:
    def __init__(self, x=True, y=True, z=True, xStepCount=200, yStepCount=200, zStepCount=200, xPath=None, yPath=None, zPath=None):

        motorOneFileName, motorTwoFileName, motorThreeFileName = findMotorPath(x=x, y=y, z=z, xPath=xPath, yPath=yPath, zPath=zPath)

        self.xEnabled = False
        self.yEnabled = False
        self.zEnabled = False
        self.xStep = xStepCount
        self.yStep = yStepCount
        self.zStep = zStepCount
        self.xPos = 0
        self.yPos = 0
        self.zPos = 0
        self.motorOne = motorOneFileName
        self.motorTwo = motorTwoFileName
        self.motorThr = motorThreeFileName

        if x:
            self.xEnabled = True
        else:
            self.xStep = 0
        if y:
            self.yEnabled = True
        else:
            self.yStep = 0
        if z:
            self.zEnabled = True
        else:
            self.zStep = 0


        self.setupMotor()

    def setupMotor(self):
        if self.xEnabled:
            Popen([self.motorOne, "xInit"])
        if self.yEnabled:
            Popen([self.motorTwo, "yInit"])
        if self.zEnabled:
            Popen([self.motorThr, "zInit"])
        print("Enabling Motors")

    def cleanupMotor(self):
        if self.xEnabled:
            Popen([self.motorOne, "xFinish"])
        if self.yEnabled:
            Popen([self.motorTwo, "yFinish"])
        if self.zEnabled:
            Popen([self.motorThr, "zFinish"])
        print("Closing Motors")

    def __del__(self):
        self.cleanupMotor()

    def getXPos(self):
        if self.xEnabled:
            return self.xPos
        return 0

    def getYPos(self):
        if self.yEnabled:
            return self.yPos
        return 0

    def getZPos(self):
        if self.zEnabled:
            return self.zPos
        return 0

    def getXStepCount(self):
        if self.xEnabled:
            return self.xStep
        return 0

    def getYStepCount(self):
        if self.yEnabled:
            return self.yStep
        return 0

    def getZStepCount(self):
        if self.zEnabled:
            return self.zStep
        return 0

    def xfw(self, step=1):
        if self.xEnabled:
            success = True
            try:
                Popen([self.motorOne, "xFullFw", str(step)])
            except:
                success = False
            if success:
                self.xPos += step
                self.xPos = self.xPos % self.xStep
                print("NEW X POS: ", self.xPos)
    def xbw(self, step=1):
        if self.xEnabled:
            success = True
            try:
                Popen([self.motorOne, "xFullBw", str(step)])
            except:
                success = False
            if success:
                self.xPos -= step
                self.xPos = (self.xPos % self.xStep)
                print("NEW X POS: ", self.xPos)

    def yfw(self, step=1):
        if self.yEnabled:
            success = True
            try:
                Popen([self.motorTwo, "yFullFw", str(step)])
            except:
                success = False
            if success:
                self.yPos += step
                self.yPos = (self.yPos % self.yStep)
                print("NEW Y POS: ", self.yPos)

    def ybw(self, step=1):
        if self.yEnabled:
            success = True
            try:
                Popen([self.motorTwo, "yFullBw", str(step)])
            except:
                success = False
            if success:
                self.yPos -= step
                self.yPos = (self.yPos % self.yStep)
                print("NEW Y POS: ", self.yPos)

    def zfw(self, step=1):
        if self.zEnabled:
            success = True
            try:
                Popen([self.motorThr, "zFullFw", str(step)])
            except:
                success = False
            if success:
                self.zPos += step
                self.zPos = (self.zPos % self.zStep)
                print("NEW Z POS: ", self.zPos)

    def zbw(self, step=1):
        if self.zEnabled:
            success = True
            try:
                Popen([self.motorThr, "zFullBw", str(step)])
            except:
                success = False
            if success:
                self.zPos -= step
                self.zPos = (self.zPos % self.zStep)
                print("NEW Z POS: ", self.zPos)

    def fullX(self, loops=1):
        Popen([self.motorOne, "Run", str(self.xStep), str(loops)])

    def fullY(self, loops=1):
        Popen([self.motorTwo, "Run", str(self.yStep), str(loops)])

    def fullZ(self, loops=1):
        Popen([self.motorThr, "Run", str(self.zStep), str(loops)])
