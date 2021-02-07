from flask import  jsonify
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from Recogniser import get_xyz_of_move, getMagnitude, getPointsWithoutStrokes, getPointsWithxyz, getRecognizer, \
    get_all_moves_in_all_dirs, get_all_moves_in_dir
from Segmenter import segment, split_arrays
import numpy as np

from classes.Activity import Activity
from classes.Dataset import Dataset
from classes.Point import Point
from classes.Sensor import Sensor


def get_FastDtw_Results_through_magnitude(filePath, recognizer):
    results = []
    testingFileMoves = segment(filePath, True)
    print("number of moves in test file =", len(testingFileMoves))
    for move in testingFileMoves:
        x, y, z = get_xyz_of_move(move)
        Magnitude = getMagnitude(x, y)
        points = getPointsWithoutStrokes(Magnitude, z)
        templateName = get_template_which_have_smallest_minimum_dist(points, recognizer, results)
        results.append(templateName)
    return results


def get_template_which_have_smallest_minimum_dist(points, recognizer, results):
    min = np.inf
    templateName = ""
    for template in recognizer.templates:
        tempPoints = template.getArrayOfPoints()
        distance, path = fastdtw(points, tempPoints, dist=euclidean)
        print("template", template.dirName, "distance = ", distance)
        if min > distance:
            min = distance
            templateName = template.dirName
    print("min =", min)
    return templateName


def get_FastDtw_Results_through_xyz(filePath, all_moves_in_all_dirs, dirNames):
    results = []
    result = ''
    testingFileMoves = segment(filePath, True)
    print("number of moves in test file =", len(testingFileMoves))
    # loop on moves inside test file
    for test_file_move in testingFileMoves:
        min = np.inf
        #loop on directories inside a list of Directories
        for i in range(len(all_moves_in_all_dirs)):
            all_moves_in_dir = all_moves_in_all_dirs[i]
            # loop on files inside each Directory
            for all_moves_in_file in all_moves_in_dir:
                # loop on moves inside each file
                for move in all_moves_in_file:
                    # print("move = ",move)
                    distance, path = fastdtw(test_file_move, move, dist=euclidean)

                    if min > distance:
                        min = distance
                        result = dirNames[i]
                    # print("result =", result, "distance = ", distance, "min =", min)
                    # print("==================================================================================")
        results.append(result)
    return results

# all_moves_in_all_dirs array(
#                               all_moves_in_dir array(
#                                                       all_moves_in_file array(
#                                                                                  move
#                                                                                  move
#                                                                               )
#                                                       all_moves_in_file array()
#                                                    )
#                               all_moves_in_dirarray()
#                            )




def fastDtw(file):
    path = "new dataset/"
    dirNames = ["pass","v", "dribbling","zigzag"]
    allDirsMoves = get_all_moves_in_all_dirs(path, dirNames)
    # recognizer = getRecognizer(allDirsMoves, dirNames)
    # results = get_FastDtw_Results_through_magnitude(file, recognizer)
    results = get_FastDtw_Results_through_xyz(file, allDirsMoves, dirNames)
    print(results)

def get_all_moves_in_subDir(dir):
    accelerometerlist = segment(dir + "/a1.txt")
    gyroscopeList = segment(dir + "/g1.txt")
    # print("number of moves in file = ", len(all_moves_in_file))
    return accelerometerlist, gyroscopeList


def getPoints(textFileName):
    timestamp, x, y, z = split_arrays(textFileName)
    points = []
    for i in range(len(x)):
        point = Point(timestamp[i], x[i], y[i], z[i])
        points.append(point)
    return points


def getMoves(dir):
    moves = []
    for j in range(1, 3):
        for i in range(1,31):
            apath = f"dataset/u{j}/{dir}/{i}/a{i}.txt"
            gpath = f"dataset/u{j}/{dir}/{i}/g{i}.txt"
            accelerometerSensor = Sensor(getPoints(apath))
            gyroscopeSensor = Sensor(getPoints(gpath))
            move = Activity(accelerometerSensor.__dict__,gyroscopeSensor.__dict__)
            moves.append(move.__dict__)
    return moves

# dataset = Dataset()
# dataset.setDataset(getMoves("dribbling"),
#                    getMoves("right pass"),
#                    getMoves("right v"),
#                    getMoves("walking"),
#                    getMoves("wrong pass 1"),
#                    getMoves("wrong pass 2"))


# import json
# # # Serializing json
# # # jsonify(dic)
# # # print(dic)
# # dict__ = dataset.__dict__
# # json_object = json.dumps(dict__)
# #
# # # Writing to sample.json
# # with open("Dataset.json", "w") as outfile:
# #     outfile.write(json_object)
#
#
# # Python program to read JSON
# # from a file
# # Opening JSON file
# with open('Dataset.json', 'r') as openfile:
#
# 	# Reading from json file
# 	dictt = json.load(openfile)
#
# from bunch import bunchify
# datasettt = Dataset()
# datasettt = bunchify(dictt)
#
#
# # print(datasettt.walking[0].accelerometer.points[0].x)
# classes = [datasettt.walking, datasettt.dribbling, datasettt.right_pass, datasettt.right_v, datasettt.walking, datasettt.wrong_pass_1, datasettt.wrong_pass_2 ]
# classNames = ["walking", "dribbling", "right_pass", "right_v", "walking", "wrong_pass_1", "wrong_pass_2" ]
# for i, classMoves in classes:
#     min = np.inf
#     for move in enumerate(classMoves):
#         pointsList = []
#         for point in move.accelerometer.points:
#             pointsList.append([point.x, point.y, point.z])
#         distance, path = fastdtw(pointsList, pointsList, dist=euclidean)
#         print("distance", distance)
