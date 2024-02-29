import graphics as g
import cv2
import math

class purePursuitPlanner:
    def __init__(self, frame, robotObj):
        self.pathPoints = []
        self.initialFrame = frame
        self.robot = robotObj
        
    def injectPoints(self, injectDistance) : 
        pathOriginalPoints = self.pathPoints.copy()
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
                    newPoint = g.coordinates(x1, curY)
                    if (newPoint.y <= y1 and newPoint.y >= y2) or (newPoint.y <= y1 and newPoint.y >= y2) : 
                        injectedPoints.append(newPoint)
            else : 
                slope = (y1 - y2)/(x1 - x2)
                y_int = y1 - slope * x1
                deltaX = math.cos(math.atan(slope)) * injectDistance
                if x1 > x2 : deltaX *= -1
                curX = x1
                while True : 
                    curX += deltaX
                    newPoint = g.coordinates(curX, (slope * curX + y_int))  
                    if((newPoint.x >= x1 and newPoint.x <= x2) or (newPoint.x >= x2 and newPoint.x <= x1)) and ((newPoint.y >= y1 and newPoint.y <= y2) or (newPoint.y >= y2 and newPoint.y <= y1)) : 
                        injectedPoints.append(newPoint)
                    else : 
                        break 
        self.pathPoints = injectedPoints.copy() 
    
    def gradientAscent(self, epoch, alpha, beta, showImg = True) : 
        newPath = []
        newPath = self.pathPoints.copy()
        for i in range(epoch) : 
            tempFrame = self.initialFrame.copy()
            for pointIndex in range(1, len(newPath) - 1): 
                # Optimizing X Coordinates
                newPath[pointIndex].x += alpha * (self.pathPoints[pointIndex].x - newPath[pointIndex].x)
                newPath[pointIndex].x += beta * (newPath[pointIndex + 1].x + newPath[pointIndex - 1].x - 2 * newPath[pointIndex].x)
                # Optimizing Y Coordinates
                newPath[pointIndex].y += alpha * (self.pathPoints[pointIndex].y - newPath[pointIndex].y)
                newPath[pointIndex].y += beta * (newPath[pointIndex + 1].y + newPath[pointIndex - 1].y - 2 * newPath[pointIndex].y)
        if showImg : 
            for point in newPath : 
                cv2.circle(tempFrame, point.convertToRaw(), 3, (255, 0, 0), -1)
            cv2.imshow("Optimizing", tempFrame)
            cv2.waitKey(0)
            
    #! Display Functions
    
    def callBackFunction(self, event, x, y, flags, paramgs) : 
        if event == cv2.EVENT_LBUTTONDOWN : 
            tempCoord = g.coordinates(0, 0)
            tempCoord.convertFromRaw(x, y)
            self.pathPoints.append(tempCoord)
    
    def createPath(self, injectDistance):
        self.pathPoints = []
        while True : 
            frame = self.initialFrame.copy()
            for point in self.pathPoints : 
                cv2.circle(frame, point.convertToRaw(), 3, (255, 0, 0), -1)
            cv2.imshow("Path Smoothing", frame)
            cv2.setMouseCallback("Path Smoothing", self.callBackFunction)
            if cv2.waitKey(1) & 0xFF == ord('f'):
                break
        # Injecting Points
        self.injectPoints(injectDistance)
        for point in self.pathPoints : 
                cv2.circle(frame, point.convertToRaw(), 3, (255, 0, 0), -1)
        cv2.imshow("Path Smoothing", frame)
        cv2.waitKey(0)
        self.gradientAscent(200, 0.1, 0.1)
        
    
    def checkCollisions(self):
        for i in range(len(self.pathPoints)-1) : 
            frame = self.initialFrame.copy()
            x1, y1, x2, y2 = self.pathPoints[i].x, self.pathPoints[i].y, self.pathPoints[i+1].x, self.pathPoints[i+1].y
            theta = math.atan((y2-y1)/(x2-x1))
            if(x2 < x1) : 
                theta = theta + math.radians(180)
            self.robot.x = self.pathPoints[i].convertToRaw()[0]
            self.robot.y = self.pathPoints[i].convertToRaw()[1]
            self.robot.theta = theta
            for point in self.pathPoints : 
                cv2.circle(frame, point.convertToRaw(), 3, (255, 0, 0), -1)
            self.robot.draw_robot(frame)
            cv2.imshow("Simulation", frame)
            cv2.waitKey(1)
            
    def  simulatePurePursuit(mainFrame):
        while True : 
            frame = mainFrame.copy()
            g.robot.theta = math.radians(45)#math.pi/180
            g.robot.draw_robot(frame)
            cv2.imshow("Simulation", frame)
            flag = False
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break