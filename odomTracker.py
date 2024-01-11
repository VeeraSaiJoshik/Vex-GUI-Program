import cv2
import cv2.aruco as aruco
import numpy as np
import os
class arucoMarker : 
    def __init__(self, corners, id):
        self.id = id
        cornerTransformed = corners.reshape((4, 2))
        (self.topLeft, self.topRight, self.bottomRight, self.bottomLeft) = cornerTransformed
        self.topLeft = (int(cornerTransformed[0][0]) ,int(cornerTransformed[0][1]))
        self.topRight = (int(cornerTransformed[1][0]) ,int(cornerTransformed[1][1]))
        self.bottomRight = (int(cornerTransformed[2][0]) ,int(cornerTransformed[2][1]))
        self.bottomLeft = (int(cornerTransformed[3][0]) ,int(cornerTransformed[3][1]))
        print((self.topLeft, self.topRight, self.bottomRight, self.bottomLeft))
    def drawAruco(self, frame, color):
        cv2.line(frame, self.topRight, self.topLeft, color, 5)
        cv2.line(frame, self.topRight, self.bottomRight, color, 5)
        cv2.line(frame, self.bottomLeft, self.bottomRight, color, 5)
        cv2.line(frame, self.bottomLeft, self.topLeft, color, 5)
def getFieldArucoPoints():
    pass
def getRobotCenter(frame, detector):
    markedFrame = frame.copy()
    greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bbox, ids, rejected = detector.detectMarkers(greyFrame)
    corners = [0, 0, 0, 0]
    print(type(ids))
    if ids is not None :
        for(markerCorner, markerID) in zip(bbox, ids) : 
            corners[int(markerID) - 1] = arucoMarker(markerCorner, markerID)
            corners[int(markerID) - 1].drawAruco(markedFrame, (0, 255, 0))
    cv2.imshow("markedFrame", markedFrame)
    print(ids)
def main():
    cap = cv2.VideoCapture(0)
    arucoDictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_100)
    arucoParamters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector( arucoDictionary, arucoParamters)
    while True :
        _, frame = cap.read()
        getRobotCenter(frame, detector)
        cv2.imshow("main", frame)
        if cv2.waitKey(1) == ord('q'):
            break
if __name__ == '__main__':
    main()