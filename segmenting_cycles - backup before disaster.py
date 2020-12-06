from dollarpy import Recognizer, Template, Point
from os import listdir
from os.path import isfile, join
import pandas as pd
import os
import math
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np




def split_arrays(textFileName):
    my_data = genfromtxt(textFileName, delimiter=',')
    accelerometerData = my_data[:, 0:4].copy()
    timestamp = accelerometerData[:, 0].copy()
    ax = accelerometerData[:, 1].copy()
    ay = accelerometerData[:, 2].copy()
    az = accelerometerData[:, 3].copy()
    return timestamp, ax, ay, az


def getdistance(x1, y1, z1, x2, y2, z2):
    distance = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) + (z1 - z2) * (z1 - z2))
    return distance


def getDistancesOfAllPoints(ax, ay, az):
    distances = []
    for i in range(len(ax)):
        if (i < len(ax) - 1):
            distances.append(getdistance(ax[i], ay[i], az[i], ax[i + 1], ay[i + 1], az[i + 1]))
    return distances


def getavgDistance(distances):
    return np.average(distances)


def plot(timestamp, distances, avg):
    distances.append(None)
    plt.plot(timestamp, distances)
    plt.plot(timestamp, avg)
    plt.ylabel('distances')
    plt.xlabel('timestamps')
    plt.show()
    # scatter distance
    plt.style.use('seaborn-whitegrid')
    plt.plot(timestamp, distances, 'o', color='black')


def getMagnitudes(ax, ay, az):
    accMagnitudeArr = []
    for i in range(len(ax)):
        axyz = [ax[i], ay[i], az[i]]
        vector = np.array(axyz)
        magnitude = np.linalg.norm(vector)
        accMagnitudeArr.append(magnitude)
        # print('row {}: magnitude = {}'.format(i,magnitude))
    return accMagnitudeArr


def movingAverage(values, window):
    weights = np.repeat(1.0, window) / window
    sma = np.convolve(values, weights, 'valid')
    return sma


def plotMagnitudeAndMovingAverage(timestamp, magnitudes, sma, magnitudePlotting=True):
    mysma = sma.copy()
    if (magnitudePlotting):
        plt.plot(timestamp, magnitudes)
    lengthDiff = len(timestamp) - len(mysma)
    for i in range(lengthDiff):
        mysma = np.append(mysma, None)
    plt.plot(timestamp, mysma)
    if (magnitudePlotting):
        plt.ylabel('Magnitude & Moving Average')
    else:
        plt.ylabel('Moving Average')
    plt.xlabel('timestamp')
    plt.show()


def plotMagnitudeAndMovingAverage(timestamp, magnitudes, sma, mode, magnitudePlotting=True):
    mysma = sma.copy()
    if (magnitudePlotting):
        plt.plot(timestamp, magnitudes)
    lengthDiff = len(timestamp) - len(mysma)
    for i in range(lengthDiff):
        mysma = np.append(mysma, None)
    plt.plot(timestamp, mysma)
    plt.plot(timestamp, mode)
    if (magnitudePlotting):
        plt.ylabel('Magnitude & Moving Average')
    else:
        plt.ylabel('Moving Average')
    plt.xlabel('timestamp')
    plt.show()


def plotMovingAverageWithThreshold(timestamp, mode, sma):
    mysma = sma.copy()
    if (len(timestamp) > len(mysma)):
        lengthDiff = len(timestamp) - len(mysma)
        for i in range(lengthDiff):
            mysma = np.append(mysma, None)
    plt.plot(timestamp, mysma)
    plt.plot(timestamp, mode)
    plt.ylabel('Moving Average & threshold')
    plt.xlabel('timestamp')
    plt.show()


def scatterMovingAverageWithThreshold(timestamp, mode, sma):
    mysma = sma.copy()
    if (len(timestamp) > len(mysma)):
        lengthDiff = len(timestamp) - len(mysma)
        for i in range(lengthDiff):
            mysma = np.append(mysma, None)
    plt.scatter(timestamp, mysma)
    plt.plot(timestamp, mode, color='orange')
    plt.ylabel('Moving Average & threshold')
    plt.xlabel('timestamp')
    plt.show()


def getWindowSummation(WindowPoints):
    sum = 0
    for point in WindowPoints:
        sum += point
    return sum


def getAllWindowsSummations(numberOfPoints, increment, sma):
    endPoint = 0
    startPoint = 0
    summations = []
    for i in range(len(sma)):
        isLengthExceeded = (i >= (len(sma) - numberOfPoints))
        if isLengthExceeded:  break
        # if looping just started dont add incrementation value
        inc = increment if i > 0 else 0
        startPoint = (i + inc - 1) if i > 0 else i
        endPoint = startPoint + numberOfPoints
        # print("inc",inc," startPoint ",startPoint," endPoint",endPoint)
        WindowPoints = sma[startPoint:endPoint]
        windowSummation = getWindowSummation(WindowPoints)
        summations.append(windowSummation)
    return summations


def getAllWindowsSummationsInIntegerType(numberOfPoints, increment, sma):
    summationsInInteger = []
    summations = getAllWindowsSummations(numberOfPoints, increment, sma)
    for s in summations:
        summationsInInteger.append(math.ceil(s))
    return summationsInInteger


def getArrayOfModes(mode, timestamp):
    modes = []
    for i in timestamp:
        if len(modes) < len(timestamp):
            modes.append(mode)
    return modes


def getIntersectionPoints(threshold, magnitude):
    intersectionPoints = []
    ctr = 0

    for i in range(len(magnitude) - 1):
        thresholdMeets = (magnitude[i] <= threshold) and (magnitude[i + 1] >= threshold)
        if (thresholdMeets):
            if ctr % 2 == 0:
                intersectionPoints.append(magnitude[i + 1])
            else:
                intersectionPoints.append(magnitude[1])
    return intersectionPoints


def getNumberOfCycles(mode, sma):
    # print("mode=", mode)
    ctr = 0
    newSMA = sma.copy()
    for i in range(len(newSMA)):
        if (newSMA[i] < mode):
            newSMA[i] = None
    return newSMA


# this is the one working to get threshhold intersections
def getintersections(mode, sma):
    # print("mode=", mode)
    intersections = []
    intersectionPoints = []
    newSMA = sma.copy()
    for i in range(len(newSMA) - 1):
        if (newSMA[i] <= mode and newSMA[i + 1] > mode) or (newSMA[i] > mode and newSMA[i + 1] <= mode):
            if (newSMA[i] <= mode and newSMA[i + 1] > mode):
                if newSMA[i] == mode:
                    intersections.append(i)
                    intersectionPoints.append(newSMA[i])
                else:
                    intersections.append(i + 1)
                    intersectionPoints.append(newSMA[i + 1])
                # print("newSMA[i+1] = ",newSMA[i+1])
            if (newSMA[i] > mode and newSMA[i + 1] <= mode):
                if newSMA[i + 1] == mode:
                    intersections.append(i + 1)
                    intersectionPoints.append(newSMA[i + 1])
                else:
                    intersections.append(i)
                    intersectionPoints.append(newSMA[i])

    return intersections, intersectionPoints


def filterFromNullPoints(smaWithNan):
    nanStart = False
    move = []
    allMoves = []
    for counter in range(len(smaWithNan) - 1):
        if (smaWithNan[counter] is None) == False:
            move.append(smaWithNan[counter])  # 1 cycle
            if nanStart == False:
                nanStart = True
        elif (smaWithNan[counter] is None) == True and (smaWithNan[counter + 1] is None) == False and nanStart == True:
            allMoves.append(move)
            move = []
    if len(move) > 0:
        allMoves.append(move)
        move = []
    return allMoves


def get_All_Moves_With_axis(allMoves, magnitudes, x, y, z):
    all_Moves_With_Zaxis = []
    for move in allMoves:
        magnitude_With_Zaxis = []
        for magnitude in move:
            index = magnitudes.index(magnitude)
            magnitude_With_Zaxis.append([x[index], y[index], z[index]])
        all_Moves_With_Zaxis.append(magnitude_With_Zaxis)

    # # for printing results
    # for i in range(len(all_Moves_With_Zaxis)):
    #   print("move ",i)
    #   for points in all_Moves_With_Zaxis[i]:
    #     print(points)
    return all_Moves_With_Zaxis


def segment(textFileName, window=2, numberOfPointsInWindow=5, increment=2, threshholdFilter = 100):
    timestamp, ax, ay, az = split_arrays(textFileName)
    magnitudes = getMagnitudes(ax, ay, az)

    sma = movingAverage(magnitudes, window)
    summations = getAllWindowsSummationsInIntegerType(numberOfPointsInWindow, increment, sma)
    # summations.sort()
    # for i in range(len(summations)-6):
    #     print(summations[i],summations[i+1],summations[i+2], summations[i+3],summations[i+4],summations[i+5],summations[i+6])
    # print("=======================================================================================================================")
    mode = max(set(summations), key=summations.count)
    print("mode = ", mode)
    modes = getArrayOfModes(mode, timestamp)
    smaWithNan = getNumberOfCycles(mode, magnitudes)

    # plotMagnitudeAndMovingAverage(timestamp, magnitudes, sma, modes, True)
    # plotMovingAverageWithThreshold(timestamp, modes, smaWithNan)
    # scatterMovingAverageWithThreshold(timestamp, modes, sma)
    # scatterMovingAverageWithThreshold(timestamp, modes, smaWithNan)

    allMoves = filterFromNullPoints(smaWithNan)
    for i in range(len(allMoves)):
        print("move ",i," ",len(allMoves[i]))
    allMoves = [i for i in allMoves if len(i) > threshholdFilter]
    # all_Moves_With_Zaxis = get_All_Moves_With_axis(allMoves, magnitudes, az)
    all_Moves_With_Zaxis = get_All_Moves_With_axis(allMoves, magnitudes, ax, ay, az)

    return all_Moves_With_Zaxis



import pandas as pd
import os
import math
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt


def split_arrays_without_timeStamps(textFileName):
    my_data = genfromtxt(textFileName, delimiter=',')
    accelerometerData = my_data[:, 0:4].copy()
    # print("ddddddddddddddddd", accelerometerData)
    timestamp = accelerometerData[:, 0].copy()
    x = accelerometerData[:, 1].copy()
    y = accelerometerData[:, 2].copy()
    z = accelerometerData[:, 3].copy()
    return x, y, z





# magnitude of xy
def getMagnitude(x, y):
    xyMagnitudes = []
    for i in range(len(x)):
        magnitude = math.sqrt(math.pow(x[i], 2) + math.pow(y[i], 2))
        xyMagnitudes.append(magnitude)
    return xyMagnitudes



def getMagnitude(x, y):
    xyMagnitudes = []
    for i in range(len(x)):
        magnitude = math.sqrt(math.pow(x[i], 2) + math.pow(y[i], 2))
        xyMagnitudes.append(magnitude)
    return xyMagnitudes


def createArray(magnitude, z):
    tempArray = []
    # print(len(magnitude))
    for i in range(len(magnitude)):
        tempArray.append(Point(magnitude[i], z[i], 1))
    return tempArray












def getRecognizer():
    mypath = "dataset/"
    dribling = [f for f in listdir(mypath + "dribling") if isfile(join(mypath + "dribling", f))]
    walking = [f for f in listdir(mypath + "walking") if isfile(join(mypath + "walking", f))]
    mypass = [f for f in listdir(mypath + "pass") if isfile(join(mypath + "pass", f))]
    zigzagMove = [f for f in listdir(mypath + "zigzagMove") if isfile(join(mypath + "zigzagMove", f))]
    v = [f for f in listdir(mypath + "v") if isfile(join(mypath + "v", f))]

    shapes = [dribling, walking, mypass, v, zigzagMove]
    # print(shapes)
    Templates = []
    for files in shapes:
        for fileName in files:
            # print(fileName)
            shapeName = fileName[:fileName.index("_")]
            fileDir = "dataset/" + shapeName + "/"
            # print("fileDir + fileName", fileDir + fileName)
            x, y, z = split_arrays_without_timeStamps(fileDir + fileName)
            magnitude = getMagnitude(x, y)
            shapeArray = createArray(magnitude, z)
            # shapeArray=segment()

            # print("shapeArray ",shapeArray)
            Templates.append(Template(shapeName, shapeArray))
            x, y, z = [],[],[]

    return Recognizer(Templates)

def getRecognizer(arrayOfzigzagMove, arrayOfPasses, arrayOfv):
    Templates = []


    # Templates.append(Template(shapeName, shapeArray))
    for allMoves in arrayOfzigzagMove:
            for k in range(len(allMoves)):
                x, y, z = [], [], []
                move = allMoves[k]
                for i in range(len(move)):
                    x.append(move[i][0])
                    y.append(move[i][1])
                    z.append(move[i][2])
            magnitude = getMagnitude(x, y)
            shapeArray = createArray(magnitude, z)
            Templates.append(Template("zigzagMove", shapeArray))

    for allMoves in arrayOfPasses:
            for k in range(len(allMoves)):
                x, y, z = [], [], []
                move = allMoves[k]
                for i in range(len(move)):
                    x.append(move[i][0])
                    y.append(move[i][1])
                    z.append(move[i][2])
            magnitude = getMagnitude(x, y)
            shapeArray = createArray(magnitude, z)
            Templates.append(Template("pass", shapeArray))

    for allMoves in arrayOfv:
            for k in range(len(allMoves)):
                x, y, z = [], [], []
                move = allMoves[k]
                for i in range(len(move)):
                    x.append(move[i][0])
                    y.append(move[i][1])
                    z.append(move[i][2])
            magnitude = getMagnitude(x, y)
            shapeArray = createArray(magnitude, z)
            Templates.append(Template("v", shapeArray))



    return Recognizer(Templates)



def predict(allMoves):
    for k in range(len(allMoves)):
        x, y, z = [], [], []
        move = allMoves[k]
        for i in range(len(move)):
            x.append(move[i][0])
            y.append(move[i][1])
            z.append(move[i][2])

        recognizer = getRecognizer()

        Magnitude = getMagnitude(x, y)
        inputArray = createArray(Magnitude, z)
        print("length of inputArray = ", len(inputArray))
        result = recognizer.recognize(inputArray)
        return result

# mypath = "dataset/"
mypath = "new dataset/"
arrayOfPasses = []
fileNames = [f for f in listdir(mypath + "zigzag") if isfile(join(mypath + "zigzag", f))]
for fileName in fileNames:
    allMoves = segment("zigzag/"+fileName)
    # if len(allMoves) == 1:
    #     arrayOfPasses.append(allMoves)
    print("number of moves in file = ", len(allMoves))
    # result = predict(allMoves)
    # print(result)
print("==================================")

# arrayOfv = []
# vMove = [f for f in listdir(mypath + "v") if isfile(join(mypath + "v", f))]
# for move in vMove:
#
#     allMoves = segment("dataset/v/"+move,40)
#     if len(allMoves) == 1:
#         arrayOfv.append(allMoves)
#     print("number of moves of v = ", len(allMoves))
#     print(move)
#     # result = predict(allMoves)
#     # print(result)
# print("==================================")
#
#
#
# arrayOfzigzagMove = []
# zigzagMove = [f for f in listdir(mypath + "zigzagMove") if isfile(join(mypath + "zigzagMove", f))]
# for move in zigzagMove:
#     allMoves = segment("dataset/zigzagMove/"+move)
#     if len(allMoves) == 1:
#         arrayOfzigzagMove.append(allMoves)
#     print("number of moves of zigzagMove = ", len(allMoves))
#     # result = predict(allMoves)
#     # print(result)
# print("========================================================================================================================================")
#
# print("arrayOfzigzagMove, arrayOfPasses, arrayOfv = ",len(arrayOfzigzagMove), len(arrayOfPasses), len(arrayOfv))
#
# #
#
#
# allMoves = segment("testing/v_5617215933977.txt")
# print("number of moves = ", len(allMoves))
# # print("number of moves = ", len(allMoves))
# for k in range(len(allMoves)):
#     x, y, z = [], [], []
#     move = allMoves[k]
#     for i in range(len(move)):
#         x.append(move[i][0])
#         y.append(move[i][1])
#         z.append(move[i][2])
#
#     recognizer = getRecognizer(arrayOfzigzagMove, arrayOfPasses, arrayOfv)
#
#     Magnitude = getMagnitude(x, y)
#     inputArray = createArray(Magnitude, z)
#     print("length of inputArray = ", len(inputArray))
#     result = recognizer.recognize(inputArray)
#     print(result)
#
# # result = predict(allMoves)
# # print(result)
# print("==================================")
#
