import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import cv2
import numpy as np
import math
# importing custom modules
import purePursuitPlanner as pp
import planning as p
import graphics as g


"""def chooseInitialPosition(event, x, y, flags, paramgs) : 
    startPosition.convertFromRaw(x, y)
def chooseInitialAngle(event, x, y, flags, paramgs):
    anglePosition.convertFromRaw(x, y)"""

# Global Variables
globalHeight = 1800
globalWidth = 1800
picelsToInches = 144.0/globalHeight
inchesToPixels = globalHeight/144.0
# Run Variables
mainFrame = np.zeros((globalHeight, globalWidth, 3), np.uint8)
fildImage = cv2.imread("fieldImage.png")
mainFrame[0:globalHeight, 0:globalHeight] = fildImage

robot = g.RobotClass(int(18 * inchesToPixels), int(15 * inchesToPixels))
robot.x = 450
robot.y = 450

g.coordinates.globalHeight = globalHeight
g.coordinates.globalWidth = globalWidth

g.pathCoordinates.globalHeight = globalHeight
g.pathCoordinates.globalWidth = globalWidth

#purePursuit = pp.purePursuitPlanner(mainFrame, robot)
#purePursuit.createPath(5)

robot.theta = math.radians(90)

pathPlanner = p.autonPlanner(mainFrame, robot)
pathPlanner.simulate()
pathPlanner.generateCode(globalHeight)