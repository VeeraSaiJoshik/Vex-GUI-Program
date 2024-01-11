import matplotlib.pyplot as plt
import numpy as np

def clampMotorSpeed(speed):
    if(speed > 200): return 200
    elif (speed < -200): return -200
    return speed
def robotRotationModel(currentVelocity):
    #return 0.12 * currentVelocity
    radiusOfWheel = 2
    radiusOfRobot = 9
    return (3.0 * radiusOfWheel * currentVelocity * 1)/(500.0*radiusOfRobot)
def simulationAlgorithm(marginOfError, angularError, kP, kI, kD):
    # for this simulation algorithm, we have to update our calculations every millisecond compared to the conventional 20 milliseconds
    xData = []
    errorData = []
    throttleData = []
    time = 0
    derivative = 0
    integral = 0
    calculateIntegral = False
    error = angularError
    prevError = angularError
    throttleSpeed = 0
    passed = False
    while(time <= 60 * 1000):
        if(abs(error) < 25): integral += error
        derivative = error - prevError
        if(error <= marginOfError and error >= -1 * marginOfError):
            passed = True
            break
        throttleSpeed = int(kP * error + kI * integral + kD * derivative)
        calculateIntegral = ((throttleSpeed == clampMotorSpeed(throttleSpeed)) and ((throttleSpeed < 0 and error < 0) or (throttleSpeed > 0 and error > 0)))
        throttleSpeed = clampMotorSpeed(throttleSpeed)
        error = error - robotRotationModel(throttleSpeed)
        prevError = error
        #print("Error : " + str(error) + "  Time : " + str(time) + " integral : " + str(integral) )
        xData.append(time)
        errorData.append(error)
        throttleData.append(throttleSpeed)
        time = time + 20
    return time, errorData, throttleData, xData, error, passed
def getAverageTime(kP, kI, kD, marginOfError):
    average = 0
    error = 10
    while error < 360: 
        time, _, _, _, e, _ = simulationAlgorithm(marginOfError, error, kP, kI, kD)
        average += time
        error += 10
    return average/35.0
def fitAndPlot(xData, yError, yThrottle):
    _, axis = plt.subplots(2, 1)
    axis[0].scatter(xData, yThrottle, label='raw Curve', color='red')
    axis[1].scatter(xData, yError, label='raw Curve', color='red')
    plt.show()
def optimize():
    f = open("data.txt", "a")
    marginOfError = 1
    kP = 0
    kI = 0
    kD = 0
    marginOfError = 1
    while(True) : 
        
        if marginOfError < 0.01 :
            break
        #! Optimizing Positional
        direction = 0
        directionStep = 1
        currentTime = getAverageTime(kP, kI, kD, marginOfError)
        directionDegree = 0
        # Finding Direction
        while True : 
            increase = getAverageTime(kP + pow(10, -1 * directionDegree), kI, kD, marginOfError)
            decrease = getAverageTime(kP - pow(10, -1 * directionDegree), kI, kD, marginOfError)
            if(increase < currentTime) : 
                direction = 1
                break
            elif(decrease < currentTime) : 
                direction = -1
                break
            else : 
                directionDegree += 1
            directionStep += 1
        print(f'Positional Direction Found : {direction}')
        # Finding the step value
        stepDegree = 0
        while True and directionDegree <= 4: 
            if stepDegree > 4 : 
                break
            curTime = getAverageTime(kP, kI, kD, marginOfError)
            newTime = getAverageTime(kP + pow(10, -1 * stepDegree) * direction, kI, kD, marginOfError)
            f.write(f'Current Kp :  {kP}  New KP : {kP + pow(10, -1 * stepDegree) * direction}  New Time : {newTime} Current Time : {currentTime} Degree : {stepDegree}\n')
            print(f'{kP}  {newTime} {stepDegree}')
            if newTime > curTime : 
                stepDegree += 1
            else : 
                kP = kP + pow(10, -1 * stepDegree) * direction
        f.write("Position Done " + str(kP))
        print("This is the margin of error : " + str(marginOfError))
        input()
        marginOfError = marginOfError * 0.5
        
    f.close()
kP = 0
x = []
y = []
time, errorData, throttleData, xData, error, passed = simulationAlgorithm(0, 90, 1.15, 0.0265, 4.2)

fitAndPlot(xData, errorData, throttleData)