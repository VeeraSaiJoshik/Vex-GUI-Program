import matplotlib.pyplot as plt
import math
def graphRPM(fileName):
    data = open(fileName)
    time = []
    bottomLeftThrottle = []
    bottomRightThrottle = []
    frontLeftThrottle = []
    frontRightThrottle = []
    for row in data : 
        tempTime, tempRearLeft, tempRearRight, tempFrontLeft, tempFrontRight = row.split(',')
        if int(tempTime)%20 == 0 : 
            time.append(int(tempTime))
            bottomLeftThrottle.append(int(float(tempRearLeft)))
            bottomRightThrottle.append(int(float(tempRearRight)))
            frontLeftThrottle.append(int(float(tempFrontLeft)))
            frontRightThrottle.append(int(float(tempFrontRight)))

    #_, axis = plt.subplots(2, 2)
    print(len(time))
    plt.plot(time, bottomLeftThrottle, c = "red", lw = 1, linestyle = "--")
    #plt.plot(time, bottomRightThrottle, c = "blue", lw = 1, linestyle = "--")
    plt.plot(time, frontLeftThrottle, c = "green", lw = 1, linestyle = "--")
    #plt.plot(time, frontRightThrottle, c = "orange", lw = 1, linestyle = "--")
    plt.show()
def graphPIDValues(fileName):
    print("graphing")
    data = open(fileName)
    TimeList = []
    CurrentPositionList = []
    TargetThrottleList = []
    ActualThrottleLeftMotorList = []
    ActualThrottleRightMotorList = []
    ActualThrottleLeftBackMotorList = []
    ActualThorttleRightBackMotorList = []
    ErrorList = []
    for row in data : 
        Time, TargetThrottle, ActualThrottleLeftMotor, ActualThrottleRightMotor, ActualThrottleLeftBackMotor, ActualThorttleRightBackMotor, Error= row.split(',')
        TimeList.append(float(Time))
        TargetThrottleList.append(float(TargetThrottle))
        ActualThrottleLeftMotorList.append(float(ActualThrottleLeftMotor))
        ActualThrottleRightMotorList.append(float(ActualThrottleRightMotor))
        ActualThrottleLeftBackMotorList.append(float(ActualThrottleLeftBackMotor))
        ActualThorttleRightBackMotorList.append(float(ActualThorttleRightBackMotor))
        ErrorList.append(math.fabs(float(Error)))

    #_, axis = plt.subplot(2, 4)
    
    """axis[0][0].plot(TimeList, ErrorList, label='Current Position List', color='red')
    axis[0][1].plot(TimeList, TargetThrottleList, label='Target Throttle', color='blue')
    axis[0][2].plot(TimeList, ActualThrottleLeftMotorList, label='Front Left Throttle', color='green')
    axis[0][3].plot(TimeList, ErrorList, label='Error', color='magenta')
    axis[1][0].plot(TimeList, ActualThrottleRightMotorList, label='Front Right Throttle', color='black')
    axis[1][1].plot(TimeList, ActualThrottleLeftBackMotorList, label='Back Left Throttle', color='orange')
    axis[1][2].plot(TimeList, ActualThorttleRightBackMotorList, label='Back Right Throttle', color='hotpink')
    axis[1][3].plot(TimeList, ErrorList, label='Error', color='magenta')"""
    
    plt.plot(TimeList, ErrorList, label = "error", color = "black")
    
    classes = ['Target', 'Error', 'Actual Right Front']
    
    plt.xlabel("Time(ms)")
    plt.ylabel("Error(deg)")  
    
    plt.legend(labels=classes)
    plt.show()

#graphRPM("data/RPM0to50.csv")
val = input()
graphPIDValues("data/rotateDataTest" + val + ".csv")