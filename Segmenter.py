from os import listdir
from os.path import isfile, join
import pandas as pd
import os
import math
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np



def segment(textFileName, plotting = False, window=2, numberOfPointsInWindow=5, increment=2, threshholdFilter=100):
    # textFileName = textFileName
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

    if plotting:
        plotMagnitudeAndMovingAverage(timestamp, magnitudes, sma, modes, True)
        plotMovingAverageWithThreshold(timestamp, modes, smaWithNan)
        scatterMovingAverageWithThreshold(timestamp, modes, sma)
        scatterMovingAverageWithThreshold(timestamp, modes, smaWithNan)

    allMoves = filterFromNullPoints(smaWithNan)
    # for i in range(len(allMoves)):
    #     print("move ", i, " ", len(allMoves[i]))
    allMoves = [i for i in allMoves if len(i) > threshholdFilter]
    all_Moves_With_axis = get_All_Moves_With_axis(allMoves, magnitudes, ax, ay, az)

    return all_Moves_With_axis

def split_arrays_without_timeStamps(textFileName):
    my_data = genfromtxt(textFileName, delimiter=',')
    accelerometerData = my_data[:, 0:4].copy()
    # print("ddddddddddddddddd", accelerometerData)
    timestamp = accelerometerData[:, 0].copy()
    x = accelerometerData[:, 1].copy()
    y = accelerometerData[:, 2].copy()
    z = accelerometerData[:, 3].copy()
    return x, y, z

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

def getAllWindowsSummations( numberOfPoints, increment, sma):
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

def getNumberOfCycles(mode, sma):
    # print("mode=", mode)
    ctr = 0
    newSMA = sma.copy()
    for i in range(len(newSMA)):
        if (newSMA[i] < mode):
            newSMA[i] = None
    return newSMA

def filterFromNullPoints(smaWithNan):
    nanStart = False
    move = []
    allMoves = []
    for counter in range(len(smaWithNan) - 1):
        if (smaWithNan[counter] is None) == False:
            move.append(smaWithNan[counter])  # 1 cycle
            if nanStart == False:
                nanStart = True
        elif (smaWithNan[counter] is None) == True and (
                smaWithNan[counter + 1] is None) == False and nanStart == True:
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

# @staticmethod
def split_arrays(textFileName):
    # print("textFileName", textFileName, " type", type(textFileName))
    my_data = genfromtxt(textFileName, delimiter=',')
    accelerometerData = my_data[:, 0:4].copy()
    timestamp = accelerometerData[:, 0].copy()
    ax = accelerometerData[:, 1].copy()
    ay = accelerometerData[:, 2].copy()
    az = accelerometerData[:, 3].copy()
    return timestamp, ax, ay, az

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


