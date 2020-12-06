from dollarpy import Recognizer, Template, Point
from os import listdir
from os.path import isfile, join
from Segmenter import segment
import pandas as pd
import os
import math
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np


# magnitude of xy
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


def getRecognizer(all_Moves_in_ever_dir, dirNames):
    Templates = getTemplates(all_Moves_in_ever_dir, dirNames)
    return Recognizer(Templates)

# go through every directory and get its templates to return dribbling_pass_v_zigzag template
def getTemplates(all_Moves_in_ever_dir, dirNames):
    Templates = []
    for i in range(len(all_Moves_in_ever_dir)):
        dirTemplates = getTemplatesInDirectory(all_Moves_in_ever_dir[i], dirNames[i])
        Templates.extend(dirTemplates)
    return Templates


def getTemplatesInDirectory(dirMoves, dirName):
    Templates = []
    for i in range(len(dirMoves)):
        fileMoves = dirMoves[i]
        for move in fileMoves:
            x, y, z = get_xyz_of_move(move)
            magnitude = getMagnitude(x, y)
            shapeArray = createArray(magnitude, z)
            template = Template(dirName, shapeArray)
            Templates.append(template)
    return Templates


def get_xyz_of_move(move):
    x, y, z = [], [], []
    for i in range(len(move)):
        x.append(move[i][0])
        y.append(move[i][1])
        z.append(move[i][2])
    return x, y, z



def getDirMoves(mypath , dirName):
    directoryMoves = []
    files = [f for f in listdir(mypath + dirName) if isfile(join(mypath + dirName, f))]
    for fileName in files:

        oneFileMoves = segment(mypath + dirName + "/" + fileName)
        directoryMoves.append(oneFileMoves)
        # print("number of moves in file = ", len(oneFileMoves))
    return directoryMoves

def getAllDirS_moves(mypath, allDirNames):
    allDirsMoves = []
    for dirName in allDirNames:
        directoryMoves = getDirMoves(mypath, dirName)
        allDirsMoves.append(directoryMoves)
    return allDirsMoves

path = "new dataset/"
dirNames = ["pass","v", "zigzag", "dribbling"]
allDirsMoves = getAllDirS_moves(path, dirNames)
recognizer = getRecognizer(allDirsMoves, dirNames)
testingFiles = files = [f for f in listdir("testing") if isfile(join("testing", f))]
# print(testingFiles)
# ['dribbling_26236934533988.txt', 'dribbling_pass_v_zigzag', 'pass_22520168256810.txt', 'v_23871390355108.txt', 'v_dribbling_125950207272103.txt', 'v_dribbling_126000007783294.txt', 'v_dribbling_pass_125874054554087.txt', 'v_dribbling_pass_125906839862844.txt', 'v_pass_125480926819218.txt', 'v_pass_125550254437232.txt', 'v_pass_125574535850360.txt', 'zigzag2_29086818904555.txt', 'zigzag_126054796959721.txt', 'zigzag_126075916544789.txt']
for file in testingFiles:
    print(file)
    testingFileMoves = segment("testing/"+file)
    print("number of moves = ", len(testingFileMoves))

    for move in testingFileMoves:
        x, y, z = get_xyz_of_move(move)
        Magnitude = getMagnitude(x, y)
        inputArray = createArray(Magnitude, z)
        print("length of inputArray = ", len(inputArray))
        result = recognizer.recognize(inputArray, 5)
        print("result = ",result)
        # for i in range(205):
        #     if i%5 == 0 and i != 0:
        #         result = recognizer.recognize(inputArray,i)
        #         print("n = ",i," result = ",result)

