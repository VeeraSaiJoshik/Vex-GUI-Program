import numpy as np
import cv2
import math


class coordinates : 
    globalHeight = 0
    globalWidth = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def convertFromRaw(self, x, y):
        self.x = x - coordinates.globalHeight/2
        self.y = coordinates.globalHeight/2 - y
    def convertToRaw(self) : 
        return (int(self.x + coordinates.globalHeight/2), int(coordinates.globalHeight/2 - self.y))
    def convertToRawX(self) : 
        return int(self.x + coordinates.globalHeight/2)
    def convertToRawY(self) : 
        return int(coordinates.globalHeight/2 - self.y)
    def __str__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"
class pathCoordinates : 
    globalHeight = 0
    globalWidth = 0
    
    def __init__(self, x, y, theta) : 
        self.x = x
        self.y = y
        self.theta = theta
    def convertFromRaw(self, x, y):
        self.x = x - pathCoordinates.globalHeight/2
        self.y = pathCoordinates.globalHeight/2 - y
    def convertToRaw(self) : 
        return (int(self.x + pathCoordinates.globalHeight/2), int(pathCoordinates.globalHeight/2 - self.y))
    def convertToRawX(self) : 
        return int(self.x + pathCoordinates.globalHeight/2)
    def convertToRawY(self) : 
        return int(pathCoordinates.globalHeight/2 - self.y)
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
        
        cv2.putText(frame, str(int(math.degrees(self.theta))), (self.x - 50, self.y - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 10)
        
        # Draw Left and Right Accleration Vector
    def setVelocityRight(self, velocity):
        pass
    def setVelocityLeft(self, velocity):  
        pass
    
"""
class autonStep:
    def __init__(self, location, angle, movementType):
        self.location = location
        self.angle = angle
        self.movementType = movementType
"""