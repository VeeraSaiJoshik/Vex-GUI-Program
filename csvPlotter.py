import matplotlib.pyplot as plt
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
        ErrorList.append(float(Error))

    
    
    """axis[0][0].scatter(TimeList, ErrorList, label='Current Position List', color='red')
    axis[0][1].scatter(TimeList, TargetThrottleList, label='Target Throttle', color='blue')
    axis[0][2].scatter(TimeList, ActualThrottleLeftMotorList, label='Front Left Throttle', color='green')
    axis[0][3].scatter(TimeList, ErrorList, label='Error', color='magenta')
    axis[1][0].scatter(TimeList, ActualThrottleRightMotorList, label='Front Right Throttle', color='black')
    axis[1][1].scatter(TimeList, ActualThrottleLeftBackMotorList, label='Back Left Throttle', color='orange')
    axis[1][2].scatter(TimeList, ActualThorttleRightBackMotorList, label='Back Right Throttle', color='hotpink')
    axis[1][3].scatter(TimeList, ErrorList, label='Error', color='magenta')"""
    #plt.scatter(x=TimeList, y=TargetThrottleList)
    plt.scatter(x=TimeList, y=ErrorList)
    #plt.scatter(x=TimeList, y=ActualThrottleLeftBackMotorList)
    classes = ['Target', 'Error', 'Actual Right Front']
    plt.legend(labels=classes)
    plt.show()
    plt.show()
#graphRPM("data/RPM0to50.csv")
val = input()
graphPIDValues("data/rotateDataTest" + val + ".csv")