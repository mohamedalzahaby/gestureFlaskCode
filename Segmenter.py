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
    # print("mode = ", mode)
    modes = getArrayOfModes(mode, timestamp)
    smaWithNan = getNumberOfCycles(mode, magnitudes)

    # if plotting:
    #     plt.switch_backend('TkAgg')  # TkAgg (instead Qt4Agg)
    #     fig, axs = plt.subplots(2)
    #     fig.suptitle('segmentation')
    #     mng = plt.get_current_fig_manager()
    #     ## works on Ubuntu??? >> did NOT working on windows
    #     mng.resize(*mng.window.maxsize())
    #     mng.window.state('zoomed')  # works fine on Windows!
    #     plotMagnitudeAndMovingAverage(timestamp, magnitudes, sma, modes, axs[0], True)
    #     plotMovingAverageWithThreshold(timestamp, modes, smaWithNan, axs[1])
    #     plt.show()
    #     plt.switch_backend('TkAgg')  # TkAgg (instead Qt4Agg)
    #     fig, axs = plt.subplots(2)
    #     fig.suptitle('segmentation')
    #     mng = plt.get_current_fig_manager()
    #     ## works on Ubuntu??? >> did NOT working on windows
    #     mng.resize(*mng.window.maxsize())
    #     mng.window.state('zoomed')  # works fine on Windows!
    #     scatterMovingAverageWithThreshold(timestamp, modes, sma, axs[0])
    #     scatterMovingAverageWithThreshold(timestamp, modes, smaWithNan, axs[1])
    #     plt.show()


    allMoves = filterFromNullPoints(smaWithNan)
    # if plotting:
    #     for i in range(len(allMoves)):
    #         print("move[", i, "] length = ", len(allMoves[i]))

    allMoves = [i for i in allMoves if len(i) > threshholdFilter]
    all_Moves_With_axis = get_All_Moves_With_axis(allMoves, magnitudes, ax, ay, az)
    # if plotting:
    #     print("all_Moves_With_axis = ",all_Moves_With_axis)

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
    newSMA = sma.copy()
    for i in range(len(newSMA)):
        if (newSMA[i] < mode):
            newSMA[i] = None
    return newSMA

def filterFromNullPoints(magnitudes):
    nanStart = False
    move = []
    allMoves = []
    for counter in range(len(magnitudes) - 1):
        if (magnitudes[counter] is None) == False:
            move.append(magnitudes[counter])  # 1 cycle
            if nanStart == False:
                nanStart = True
        elif (magnitudes[counter] is None) == True and (
                magnitudes[counter + 1] is None) == False and nanStart == True:
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

def plotMagnitudeAndMovingAverage(timestamp, magnitudes, sma, mode, axs, magnitudePlotting=True ):
    mysma = sma.copy()
    if (magnitudePlotting):
        axs.plot(timestamp, magnitudes)
    lengthDiff = len(timestamp) - len(mysma)
    for i in range(lengthDiff):
        mysma = np.append(mysma, None)
    axs.plot(timestamp, mysma)
    axs.plot(timestamp, mode)
    if (magnitudePlotting):
        plt.ylabel('Magnitude & Moving Average')
    else:
        plt.ylabel('Moving Average')
    plt.xlabel('timestamp')

def plotMovingAverageWithThreshold(timestamp, mode, sma, axs):
    mysma = sma.copy()
    if (len(timestamp) > len(mysma)):
        lengthDiff = len(timestamp) - len(mysma)
        for i in range(lengthDiff):
            mysma = np.append(mysma, None)
    axs.plot(timestamp, mysma)
    axs.plot(timestamp, mode)
    plt.ylabel('Moving Average & threshold')
    plt.xlabel('timestamp')

def scatterMovingAverageWithThreshold(timestamp, mode, sma, axs):
    mysma = sma.copy()
    if (len(timestamp) > len(mysma)):
        lengthDiff = len(timestamp) - len(mysma)
        for i in range(lengthDiff):
            mysma = np.append(mysma, None)
    axs.scatter(timestamp, mysma)
    axs.plot(timestamp, mode, color='orange')
    plt.ylabel('Moving Average & threshold')
    plt.xlabel('timestamp')

def getWindowSummation(WindowPoints):
    sum = 0
    for point in WindowPoints:
        sum += point
    return sum


