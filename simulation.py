import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import cv2
import numpy as np
import math
# All Classes
class coordinates : 
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def convertFromRaw(self, x, y):
        self.x = x - globalHeight/2
        self.y = globalHeight/2 - y
    def convertToRaw(self) : 
        return (int(self.x + globalHeight/2), int(globalHeight/2 - self.y))
    def convertToRawX(self) : 
        return int(self.x + globalHeight/2)
    def convertToRawY(self) : 
        return int(globalHeight/2 - self.y)
    def __str__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"
class pathCoordinates : 
    def __init__(self, x, y, theta) : 
        self.x = x
        self.y = y
        self.theta = theta
    def convertFromRaw(self, x, y):
        self.x = x - globalHeight/2
        self.y = globalHeight/2 - y
    def convertToRaw(self) : 
        return (int(self.x + globalHeight/2), int(globalHeight/2 - self.y))
    def convertToRawX(self) : 
        return int(self.x + globalHeight/2)
    def convertToRawY(self) : 
        return int(globalHeight/2 - self.y)
    def __str__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"
class RobotClass :
    def __init__(self, w, h):
        # Global Position Variables
        self.x = 0
        self.y = 0
        self.theta = 0
        # Dimension Variables
        self.width = w
        self.height = h
        # Speed Variables
        self.rightSpeed = 0
        self.leftSpeed = 0
        self.linearVelocity = 0
        self.linearAcceleration = 0
        self.angularVelocity = 0
        self.angularAcceleration = 0
    def draw_robot(self, frame):
        # drawing robot frame
        topLeft = (
            self.x + int(math.sin(math.atan(self.width/self.height) - self.theta) * math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2))), 
            self.y - int(math.cos(math.atan(self.width/self.height) - self.theta) * math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2)))
        )
        topRight = (
            self.x + int(math.sin(math.atan(self.width/self.height) + self.theta) * math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2))), 
            self.y + int(math.cos(math.atan(self.width/self.height) + self.theta) * math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2)))
        )
        bottomLeft = (
            self.x - int(math.sin(math.atan(self.width/self.height) + self.theta) * math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2))), 
            self.y - int(math.cos(math.atan(self.width/self.height) + self.theta) * math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2)))
        )
        bottomRight = (
            self.x - int(math.sin(math.atan(self.width/self.height) - self.theta) * math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2))), 
            self.y + int(math.cos(math.atan(self.width/self.height) - self.theta) * math.sqrt(math.pow(self.width/2, 2) + math.pow(self.height/2, 2)))
        )
        # Draw Robot
        # Filling in Robot
        yShift = 0
        xShift = 0
        shiftIndex = 0
        verticalShift = False
        borderWidth = 1
        if topLeft[1] - bottomLeft[1] == 0 or topLeft[0] - topRight[0] == 0: 
            yShift = 0
            xShift = 1
            shiftIndex = self.width
          #  print("d2")
            if((topLeft[0] - bottomLeft[0]) < 0): xShift = -1
            
        elif topLeft[0] - bottomLeft[0] == 0 : 
            xShift = 0
            yShift = -1
            shiftIndex = self.height
           # print("d1")
            if((topLeft[1] - bottomLeft[1]) < 0): yShift = 1
        else : 
            # Horizontal Shift
            xShift = 1
            yShift = (topLeft[1] - bottomLeft[1])/(topLeft[0] - bottomLeft[0]) 
            if topLeft[0] > bottomLeft[0] : yShift *= -1
            shiftIndex = abs(math.cos(self.theta) * self.width)
            if((topLeft[0] - bottomLeft[0]) < 0): xShift = -1
            borderWidth = self.width/shiftIndex
            # Vertical Shift
            if abs((topLeft[1] - topRight[1])/(topLeft[0] - topRight[0])) < abs(yShift):
                verticalShift = True
                yShift = (topLeft[1] - topRight[1])/(topLeft[0] - topRight[0])
                if(topLeft[0] < topRight[0]) : yShift *= -1
                if(topLeft[0] < topRight[0]) : xShift = 1
                else : xShift = -1
                shiftIndex = abs(math.sin(self.theta) * self.height)
                borderWidth = self.height/shiftIndex
           # print("d3")
            
            
        if borderWidth > 1 : borderWidth = 2
        for i in range(1, int(shiftIndex)) : 
            if verticalShift : cv2.line(frame, (int(topLeft[0] + xShift * i), int(topLeft[1] - yShift * i)), (int(bottomLeft[0] + xShift * i), int(bottomLeft[1] - yShift * i)), (0, 255, 0), abs(int(borderWidth)))
            else : cv2.line(frame, (int(topLeft[0] - xShift * i), int(topLeft[1] + yShift * i)), (int(topRight[0] - xShift * i), int(topRight[1] + yShift * i)), (0, 255, 0), abs(int(borderWidth)))
        # Drawing Edges
        if shiftIndex < 2 : shiftIndex = 2
        cv2.line(frame, topLeft, topRight, (0, 0, 255), abs(int(1)))
        cv2.line(frame, topLeft, bottomLeft, (0, 0, 255), abs(int(1)))
        cv2.line(frame, bottomLeft, bottomRight, (0, 0, 255), abs(int(1)))
        cv2.line(frame, bottomRight, topRight, (0, 0, 255), abs(int(1)))
        # Filling in Edges
        np.zeros((2, self.height - 2))
        # Drawing Corners
        cv2.circle(frame, topLeft, 5, (0, 255, 0), -1)
        cv2.circle(frame, topRight, 5, (0, 255, 0), -1)
        cv2.circle(frame, bottomRight, 5, (0, 255, 0), -1)
        cv2.circle(frame, bottomLeft, 5, (0, 255, 0), -1)
        # Draw Center and Forward
        cv2.circle(frame, (self.x, self.y), 5, (0, 255, 0), -1)
        cv2.line(frame, (self.x, self.y), (int(self.x + math.cos(self.theta) * (self.height * 1/2 + 20)), int(self.y - math.sin(self.theta) * (self.height * 1/2 + 20))), (255, 0, 0), 5)
        # Draw Left and Right Accleration Vector
    def setVelocityRight(self, velocity):
        pass
    def setVelocityLeft(self, velocity):  
        pass

# Global Functions
# Path Creation Functions
def injectPoints(path, injectDistance) : 
    injectedPoints = []
    for i in range(len(pathOriginalPoints) - 1) : 
        p1 = pathOriginalPoints[i]
        p2 = pathOriginalPoints[i + 1]
        x1, y1, x2, y2 = [p1.x, p1.y, p2.x, p2.y]
        if x1 == x2 : 
            curY = y1
            direction = -1
            if y1 < y2 : direction = 1
            while True : 
                curY = curY + direction * injectDistance
                newPoint = coordinates(x1, curY)
                if (newPoint.y <= y1 and newPoint.y >= y2) or (newPoint.y <= y1 and newPoint.y >= y2) : 
                    injectedPoints.append(newPoint)
        else : 
            slope = (y1 - y2)/(x1 - x2)
            y_int = y1 - slope * x1
            #print(y_int)
            deltaX = math.cos(math.atan(slope)) * injectDistance
            if x1 > x2 : deltaX *= -1
            curX = x1
            #print(deltaX, curX)
            while True : 
                curX += deltaX
                #print(p1, p2)
                #print("slope : " + str(slope))
                newPoint = coordinates(curX, (slope * curX + y_int))  
                #print((newPoint.x, newPoint.y))
                if((newPoint.x >= x1 and newPoint.x <= x2) or (newPoint.x >= x2 and newPoint.x <= x1)) and ((newPoint.y >= y1 and newPoint.y <= y2) or (newPoint.y >= y2 and newPoint.y <= y1)) : 
                    injectedPoints.append(newPoint)
                else : 
                    break  
    return injectedPoints
def gradientAscent(path, epoch, alpha, beta, frame) : 
    newPath = []
    newPath = path.copy()
    for i in range(epoch) : 
        
        tempFrame = frame.copy()
        for pointIndex in range(1, len(newPath) - 1): 
            # Optimizing X Coordinates
            newPath[pointIndex].x += alpha * (path[pointIndex].x - newPath[pointIndex].x)
            newPath[pointIndex].x += beta * (newPath[pointIndex + 1].x + newPath[pointIndex - 1].x - 2 * newPath[pointIndex].x)
            # Optimizing Y Coordinates
            newPath[pointIndex].y += alpha * (path[pointIndex].y - newPath[pointIndex].y)
            newPath[pointIndex].y += beta * (newPath[pointIndex + 1].y + newPath[pointIndex - 1].y - 2 * newPath[pointIndex].y)
        #print("epoch : " + str(i))
        #print(len(newPath))
    for point in newPath : 
        cv2.circle(tempFrame, point.convertToRaw(), 3, (255, 0, 0), -1)
    cv2.imshow("optimizing", tempFrame)
    cv2.waitKey(0)
    return newPath
def smoothenPath(ogFrame, injectDistance):
    global pathOriginalPoints
    pathOriginalPoints = []    
    while True : 
        frame = ogFrame.copy()
        for point in pathOriginalPoints : 
            cv2.circle(frame, point.convertToRaw(), 3, (255, 0, 0), -1)
        cv2.imshow("Original Image", frame)
        cv2.setMouseCallback("Original Image", mousePoints)
        if cv2.waitKey(1) & 0xFF == ord('f'):
            break
    # Injecting Points
    injectedPoints = injectPoints(pathOriginalPoints, injectDistance)
    for point in injectedPoints : 
            cv2.circle(frame, point.convertToRaw(), 3, (255, 0, 0), -1)
    cv2.imshow("Original Image", frame)
    cv2.waitKey(0)
    finalPath = gradientAscent(injectedPoints, 200, 0.1, 0.1, ogFrame)
    return finalPath
def checkCollisions(path, bot, ogFrame):
    for i in range(len(path)-1) : 
        frame = ogFrame.copy()
        x1, y1, x2, y2 = path[i].x, path[i].y, path[i+1].x, path[i+1].y
        theta = math.atan((y2-y1)/(x2-x1))
        if(x2 < x1) : 
            theta = theta + math.radians(180)
        bot.x = path[i].convertToRaw()[0]
        bot.y = path[i].convertToRaw()[1]
        bot.theta = theta
        for point in path : 
            cv2.circle(frame, point.convertToRaw(), 3, (255, 0, 0), -1)
        bot.draw_robot(frame)
        cv2.imshow("Sim", frame)
        cv2.waitKey(1)
def  simulatePurePursuit(mainFrame):
    while True : 
        frame = mainFrame.copy()
        robot.theta = math.radians(45)#math.pi/180
        robot.draw_robot(frame)
        cv2.imshow("main", frame)
        flag = False
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
def mousePoints(event, x, y, flags, paramgs) : 
    if event == cv2.EVENT_LBUTTONDOWN : 
        tempCoord = coordinates(0, 0)
        tempCoord.convertFromRaw(x, y)
        pathOriginalPoints.append(tempCoord)
def chooseInitialPosition(event, x, y, flags, paramgs) : 
    startPosition.convertFromRaw(x, y)
def chooseInitialAngle(event, x, y, flags, paramgs):
    anglePosition.convertFromRaw(x, y)
# Path Planning

def pathPlanning(ogFrame):
    global startPosition
    global startTheta 
    global anglePosition
    global flag
    flag = False
    startTheta = 0
    startPosition = coordinates(0, 0)
    sliderImage = np.zeros((100,520,3), np.uint8)
    # Choosing Position
    while(True):
        frame = ogFrame.copy()
        
        robot.x = startPosition.convertToRaw()[0]
        robot.y = startPosition.convertToRaw()[1]
        if startPosition.x != 0 and startPosition.y != 0 : 
            robot.draw_robot(frame)
        cv2.imshow("Original Image", frame)
        cv2.setMouseCallback("Original Image", chooseInitialPosition)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    # Choosing Angle
    anglePosition = coordinates(0, 0)
    while(True):
        frame = ogFrame.copy()
        
        deltaX = anglePosition.x - startPosition.x
        deltaY = anglePosition.y - startPosition.y
        if deltaX == 0: 
            if deltaY > 0 : 
                robot.theta = math.radians(90)
            else : 
                robot.theta = math.radians(180)
        else : 
            robot.theta = abs(math.atan(deltaY/deltaX))
            if deltaX > 0 and deltaY > 0: 
                robot.theta += 0
            elif deltaX < 0 and deltaY > 0: 
                robot.theta = math.radians(180) - robot.theta
            elif deltaX < 0 and deltaY < 0: 
                robot.theta = math.radians(180) + robot.theta
            elif deltaX > 0 and deltaY < 0: 
                robot.theta = math.radians(360) - robot.theta
            print(math.degrees(robot.theta))
            robot.draw_robot(frame)
            cv2.line(frame, (robot.x, robot.y), (int(anglePosition.convertToRawX()), int(anglePosition.convertToRawY())), (0,0,255), 3)
            #cv2.line(frame, (robot.x, robot.y), (int(robot.x + deltaX), robot.y), (0,0,255), 3)
            #cv2.line(frame, (int(robot.x + deltaX), robot.y), (int(robot.x + deltaX), int(robot.y - deltaY)), (0,0,255), 3)
        
        
        cv2.imshow("Original Image", frame)
        cv2.setMouseCallback("Original Image", chooseInitialAngle)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    pointsList = [
        pathCoordinates(startPosition.x, startPosition.y, robot.theta)
    ]
    while(True):
        frame = ogFrame.copy()
        # Display Past Location
        # Choose Location
        # Choose Angle
        cv2.imshow("Original Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    
# Global Variables
globalHeight = 1800
globalWidth = 1800
picelsToInches = 144.0/globalHeight
inchesToPixels = globalHeight/144.0
# Run Variables
mainFrame = np.zeros((globalHeight, globalWidth, 3), np.uint8)
fildImage = cv2.imread("fieldImage.png")
mainFrame[0:globalHeight, 0:globalHeight] = fildImage
robot = RobotClass(int(19 * inchesToPixels), int(17.5 * inchesToPixels))
robot.x = 450
robot.y = 450
#simulatePurePursuit(mainFrame)
#finalPath = smoothenPath(mainFrame, 10)
#checkCollisions(finalPath, robot, mainFrame)
pathPlanning(mainFrame)
