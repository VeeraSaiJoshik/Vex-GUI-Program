import graphics as g
import numpy as np
import math
import cv2
import graphics as g
from enum import Enum

"""
TODO : 
    - Create The following intake functions
        - Intake
        - Outtake
        - Puncher
    - Convert the path list to 'movement list'
        - Convert 'movement list' to c++ code
    - Create Functionality to move points
?DOING :
    - Create Functionality in order to place Circle Markers with letters in them around the field to represent object interaction
*DONE :
    - Display Angle on Robot
    - Create Functionality for robot to rotate as dragging around filed
        - Map this to the F key
    - Create Functionality to move the robot backwards
        - Map this to the B key
"""

class Mode(Enum):
    MOVEF = 1
    MOVEB = 5
    ROTATE = 2
    QUIT = 3
    IDLE = 4
    OUTTAKE = 10
    INTAKE = 6
    PUNCH = 7

class autonStep:
    def __init__(self, location, angle, movementType):
        self.location = location
        self.angle = angle
        self.movementType = movementType
        
class autonPlanner:
    def __init__(self, frame, robot, ):
        self.originalFrame = frame
        self.frame = frame.copy()
        self.robot = robot
        
        self.chooseMode = Mode.MOVEF
        
        self.pathList = [] 
        self.mouseCoordinate = g.coordinates(0, 0)
        
    def callbackFunction(self, event, x, y, flags, paramgs) : 
        self.mouseCoordinate.convertFromRaw(x, y)
        print(event)
        if event == 1:
            curLoc = g.coordinates(0, 0)
            curLoc.convertFromRaw(self.robot.x, self.robot.y)
            self.pathList.append(
                autonStep(
                    curLoc,
                    self.robot.theta, 
                    self.chooseMode
                )  
            )
            self.chooseMode = Mode.IDLE
    def chooseLocationForward(self):
        while(True):
            frame = self.frame.copy() 
            
            self.robot.x = self.mouseCoordinate.convertToRaw()[0]
            self.robot.y = self.mouseCoordinate.convertToRaw()[1]
            
            # Drawing Grid Lines
            
            h, w, _ = frame.shape
            
            cv2.line(frame, (0, self.robot.y), (self.robot.x, self.robot.y), (0, 0, 0), 5)
            cv2.line(frame, (w, self.robot.y), (self.robot.x, self.robot.y), (0, 0, 0), 5)
            cv2.line(frame, (self.robot.x, 0), (self.robot.x, self.robot.y), (0, 0, 0), 5)
            cv2.line(frame, (self.robot.x, h), (self.robot.x, self.robot.y), (0, 0, 0), 5)
            
#            print(self.robot.x, self.robot.y)
            if len(self.pathList) != 0 : cv2.line(frame, (self.robot.x, self.robot.y), (self.pathList[-1].location.convertToRawX(), self.pathList[-1].location.convertToRawY()), (0,0,255), 3)
            if len(self.pathList) != 0 : 
                curLoc = g.coordinates(0, 0)

                curLoc.convertFromRaw(self.robot.x , self.robot.y)

                deltaX = curLoc.x - self.pathList[-1].location.x
                deltaY = curLoc.y - self.pathList[-1].location.y
                
                
                if deltaX == 0: 
                    if deltaY > 0 : 
                        self.robot.theta = math.radians(90)
                    else : 
                        self.robot.theta = math.radians(270)
                else : 
                    self.robot.theta = abs(math.atan(deltaY/deltaX))
                    if deltaX > 0 and deltaY > 0: 
                        self.robot.theta += 0
                    elif deltaX < 0 and deltaY > 0: 
                        self.robot.theta = math.radians(180) - self.robot.theta
                    elif deltaX < 0 and deltaY < 0: 
                        self.robot.theta = math.radians(180) + self.robot.theta
                    elif deltaX > 0 and deltaY < 0: 
                        self.robot.theta = math.radians(360) - self.robot.theta
            
            self.robot.draw_robot(frame)
            
            cv2.imshow("Original Image", frame)
            cv2.setMouseCallback("Original Image", self.callbackFunction)
            
            key = cv2.waitKey(1)
            
            if self.chooseMode == Mode.IDLE : 
                cv2.destroyAllWindows()
                break
    def chooseLocationBackward(self):
        while(True):
            frame = self.frame.copy() 
            
            self.robot.x = self.mouseCoordinate.convertToRaw()[0]
            self.robot.y = self.mouseCoordinate.convertToRaw()[1]
            
            # Drawing Grid Lines
            
            h, w, _ = frame.shape
            
            cv2.line(frame, (0, self.robot.y), (self.robot.x, self.robot.y), (0, 0, 0), 5)
            cv2.line(frame, (w, self.robot.y), (self.robot.x, self.robot.y), (0, 0, 0), 5)
            cv2.line(frame, (self.robot.x, 0), (self.robot.x, self.robot.y), (0, 0, 0), 5)
            cv2.line(frame, (self.robot.x, h), (self.robot.x, self.robot.y), (0, 0, 0), 5)
            
#            print(self.robot.x, self.robot.y)
            if len(self.pathList) != 0 : cv2.line(frame, (self.robot.x, self.robot.y), (self.pathList[-1].location.convertToRawX(), self.pathList[-1].location.convertToRawY()), (0,0,255), 3)
            if len(self.pathList) != 0 : 
                curLoc = g.coordinates(0, 0)

                curLoc.convertFromRaw(self.robot.x , self.robot.y)

                deltaX = curLoc.x - self.pathList[-1].location.x
                deltaY = curLoc.y - self.pathList[-1].location.y
                
                
                if deltaX == 0: 
                    if deltaY > 0 : 
                        self.robot.theta = math.radians(90)
                    else : 
                        self.robot.theta = math.radians(270)
                else : 
                    self.robot.theta = abs(math.atan(deltaY/deltaX))
                    if deltaX > 0 and deltaY > 0: 
                        self.robot.theta += 0
                    elif deltaX < 0 and deltaY > 0: 
                        self.robot.theta = math.radians(180) - self.robot.theta
                    elif deltaX < 0 and deltaY < 0: 
                        self.robot.theta = math.radians(180) + self.robot.theta
                    elif deltaX > 0 and deltaY < 0: 
                        self.robot.theta = math.radians(360) - self.robot.theta
            
            self.robot.theta += math.radians(180)
            
            self.robot.draw_robot(frame)
            
            cv2.imshow("Original Image", frame)
            cv2.setMouseCallback("Original Image", self.callbackFunction)
            
            key = cv2.waitKey(1)
            
            if self.chooseMode == Mode.IDLE : 
                cv2.destroyAllWindows()
                break
    def chooseOrientation(self):
        while(True):
            frame = self.frame.copy()
            
            deltaX = self.mouseCoordinate.convertToRawX() - self.robot.x
            deltaY = -1 * self.mouseCoordinate.convertToRawY() + self.robot.y
            if deltaX == 0: 
                if deltaY > 0 : 
                    self.robot.theta = math.radians(90)
                else : 
                    self.robot.theta = math.radians(270)
            else : 
                self.robot.theta = abs(math.atan(deltaY/deltaX))
                if deltaY == 0 :
                    if deltaX > 0 : 
                        self.robot.theta = 0
                    else : 
                        self.robot.theta = math.radians(180)
                elif deltaX > 0 and deltaY > 0: 
                    self.robot.theta += 0
                elif deltaX < 0 and deltaY > 0: 
                    self.robot.theta = math.radians(180) - self.robot.theta
                elif deltaX < 0 and deltaY < 0: 
                    self.robot.theta = math.radians(180) + self.robot.theta
                elif deltaX > 0 and deltaY < 0: 
                    self.robot.theta = math.radians(360) - self.robot.theta
            
            #print(int(math.degrees(self.robot.theta)))
            self.robot.draw_robot(frame)
            cv2.line(frame, (self.robot.x, self.robot.y), (int(self.mouseCoordinate.convertToRawX()), int(self.mouseCoordinate.convertToRawY())), (0,0,255), 3)            
            
            cv2.imshow("Original Image", frame)
            cv2.setMouseCallback("Original Image", self.callbackFunction)
            
            key = cv2.waitKey(1)
            
            if self.chooseMode == Mode.IDLE:
                cv2.destroyAllWindows()
                break
    
    def drawPath(self):
        self.frame = self.originalFrame.copy()
        
        cv2.circle(self.frame, (self.pathList[0].location.convertToRawX(), self.pathList[0].location.convertToRawY()), 20, (0, 255, 0), -1)
        
        for i in range(1, len(self.pathList)):
            if self.pathList[i].movementType == Mode.MOVEF :
                cv2.line(self.frame, (self.pathList[i].location.convertToRawX(), self.pathList[i].location.convertToRawY()), (self.pathList[i-1].location.convertToRawX(), self.pathList[i-1].location.convertToRawY()), (0, 0, 255), 10)
                cv2.circle(self.frame, (self.pathList[i].location.convertToRawX(), self.pathList[i].location.convertToRawY()), 20, (0, 255, 0), -1)
                cv2.circle(self.frame, (self.pathList[i - 1].location.convertToRawX(), self.pathList[i - 1].location.convertToRawY()), 20, (0, 255, 0), -1)
            if self.pathList[i].movementType == Mode.MOVEB :
                cv2.line(self.frame, (self.pathList[i].location.convertToRawX(), self.pathList[i].location.convertToRawY()), (self.pathList[i-1].location.convertToRawX(), self.pathList[i-1].location.convertToRawY()), (203, 204, 255), 10)
                cv2.circle(self.frame, (self.pathList[i].location.convertToRawX(), self.pathList[i].location.convertToRawY()), 20, (0, 255, 0), -1)
                cv2.circle(self.frame, (self.pathList[i - 1].location.convertToRawX(), self.pathList[i - 1].location.convertToRawY()), 20, (0, 255, 0), -1)
            elif self.pathList[i].movementType == Mode.ROTATE :
                cv2.line(self.frame, (self.pathList[i].location.convertToRawX(), self.pathList[i].location.convertToRawY()), (self.pathList[i].location.convertToRawX() + int(math.cos(self.pathList[i].angle) * 100), self.pathList[i].location.convertToRawY() - int(math.sin(self.pathList[i].angle) * 100)), (255, 0, 0), 5)
        for i in range(1, len(self.pathList)):
            if self.pathList[i].movementType == Mode.INTAKE:
                cv2.circle(self.frame, (self.pathList[i].location.convertToRawX(), self.pathList[i].location.convertToRawY()), 40, (230, 216, 173), -1)
                cv2.putText(self.frame, "I", (self.pathList[i].location.convertToRawX() - 10, self.pathList[i].location.convertToRawY() + 20), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 7)
            elif self.pathList[i].movementType == Mode.OUTTAKE:
                cv2.circle(self.frame, (self.pathList[i].location.convertToRawX(), self.pathList[i].location.convertToRawY()), 40, (230, 216, 173), -1)
                cv2.putText(self.frame, "O", (self.pathList[i].location.convertToRawX() - 20, self.pathList[i].location.convertToRawY() + 20), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 7)
            elif self.pathList[i].movementType == Mode.PUNCH:
                cv2.circle(self.frame, (self.pathList[i].location.convertToRawX(), self.pathList[i].location.convertToRawY()), 40, (230, 216, 173), -1)
                cv2.putText(self.frame, "P", (self.pathList[i].location.convertToRawX() - 10, self.pathList[i].location.convertToRawY() + 20), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 7)
            
                    
    def simulate(self):
        while(True):
            while(True):
                if len(self.pathList) != 0 : self.drawPath()
                
                cv2.imshow("Idle", self.frame)
                key = cv2.waitKey(1)
                
                if key != -1 :
                    keyChar = chr(key & 0xff)
                    if keyChar.lower() == 'f' : 
                        self.chooseMode = Mode.MOVEF
                    elif keyChar.lower() == 'r' : 
                        self.chooseMode = Mode.ROTATE
                    elif keyChar.lower() == 'b' : 
                        self.chooseMode = Mode.MOVEB
                    elif keyChar.lower() == 'q' : 
                        self.chooseMode = Mode.QUIT
                    elif keyChar.lower() == 'i' : 
                        self.chooseMode = Mode.INTAKE
                    elif keyChar.lower() == 'o' : 
                        self.chooseMode = Mode.OUTTAKE
                        print("outtaken chosen")
                    elif keyChar.lower() == 'p' : 
                        self.chooseMode = Mode.PUNCH
                    # Calculating Angle
                    finalTheta = 0
                    finalCoordinate = g.coordinates(self.robot.x, self.robot.y)
                    finalCoordinate.convertFromRaw(self.robot.x, self.robot.y)
                    
                    cv2.destroyAllWindows()
                    break
            
            if self.chooseMode == Mode.MOVEF : 
                self.chooseLocationForward()
            elif self.chooseMode == Mode.ROTATE :
                self.chooseOrientation()
            elif self.chooseMode == Mode.MOVEB: 
                self.chooseLocationBackward()
            elif self.chooseMode == Mode.INTAKE: 
                print("intake time")
                tempCoords = g.coordinates(self.robot.x, self.robot.y)
                tempCoords.convertFromRaw(self.robot.x, self.robot.y)
                self.pathList.append(
                    autonStep(
                       tempCoords,
                       self.robot.theta, 
                       self.chooseMode 
                    )
                )
            elif self.chooseMode == Mode.OUTTAKE: 
                print("outtake time")
                tempCoords = g.coordinates(self.robot.x, self.robot.y)
                tempCoords.convertFromRaw(self.robot.x, self.robot.y)
                self.pathList.append(
                    autonStep(
                       tempCoords, 
                       self.robot.theta, 
                       self.chooseMode 
                    )
                )
            elif self.chooseMode == Mode.PUNCH: 
                tempCoords = g.coordinates(self.robot.x, self.robot.y)
                tempCoords.convertFromRaw(self.robot.x, self.robot.y)
                self.pathList.append(
                    autonStep(
                       tempCoords, 
                       self.robot.theta, 
                       self.chooseMode 
                    )
                )
            else : 
                break
            for p in self.pathList : 
                print("=====")
                print(p.location.convertToRawY())
                print(p.location.convertToRawX())
    # this function is in degrees
    def getReferenceAngle(self, angle):
        refAngle = 0
        if angle >= 0 and angle <= 90 : 
            refAngle = angle
        elif angle >= 90 and angle <= 180 : 
            refAngle = 180 - angle
        elif angle >= 180 and angle <= 270 : 
            refAngle = angle - 180
        else : 
            refAngle = 360 - angle
        return refAngle
    # this function is in degree
    def transformReferenceAngle(self, angle):
        refAngle = self.getReferenceAngle(angle)
        finalAngle = 0
        if angle >= 0 and angle <= 90 :
            finalAngle = 90 - refAngle
        elif angle >= 90 and angle <= 180 :
            finalAngle = 270 + refAngle
        elif angle >= 180 and angle <= 270 :
            finalAngle = 270 - refAngle
        else : 
            finalAngle = 90 + refAngle
        return finalAngle
    
    def findError(self, a1, a2):
        # Calculate angular distance
        distance = abs(a1 - a2)

        # Ensure the result is within the range [0, 360) degrees
        distance = distance % 360

        return distance
    
    def generateCode(self, globalHeight):
        code = ""
        
        for i in range(1, len(self.pathList)) : 
            move = self.pathList[i]
            if move.movementType == Mode.MOVEF : 
                print("angles : ")
                angularError = self.findError(self.transformReferenceAngle(math.degrees(self.pathList[i - 1].angle)), self.transformReferenceAngle(math.degrees(move.angle)))
                print("angular error : " + str(int(angularError)))
                if(angularError > 3):
                    code += "rotateRobotTo(" + str(self.transformReferenceAngle(math.degrees(move.angle))) + ");\n"
                distance = math.sqrt(math.pow((self.pathList[i - 1].location.convertToRawX() - move.location.convertToRawX()), 2)+math.pow((self.pathList[i - 1].location.convertToRawY() - move.location.convertToRawY()), 2)) * 144.0/globalHeight
                code += "moveRobotByPID(" + str(int(distance)) + ");\n"
            elif move.movementType == Mode.INTAKE : 
                code += "runIntake(400);\n"
            elif move.movementType == Mode.ROTATE : 
                code += "rotateRobotTo(" + str(int(self.transformReferenceAngle(math.degrees(move.angle)))) + ");\n"
            elif move.movementType == Mode.OUTTAKE : 
                code += "runOuttake(400);\n"
            elif move.movementType == Mode.PUNCH : 
                pass
        print(code)
                