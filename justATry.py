import math
import statistics
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt

from Recogniser import get_all_moves_in_all_dirs
from Segmenter import segment, split_arrays, getMagnitudes, plotMovingAverageWithThreshold

# importing pandas as pd
import pandas as pd


def get_points(timestamp, x, y, z):
    points = []
    for i in range(len(timestamp)):
        point = [x[i], y[i], z[i]]
        points.append(point)
    return points


def get_segmented_points_by_Euclidean(file, segmentPoint=2080):
    timestamp, x, y, z = split_arrays(file)
    # magnitudes = getMagnitudes(x, y, z)
    # print("number of t = ",len(timestamp))
    sum = 0
    points = get_points(timestamp, x, y, z)
    stopIndex = 0
    for i in range(len(points)-1):
        point1 = points[i]
        point2 = points[i + 1]
        dist1 = np.array((point1[0], point1[1], point1[2]))
        dist2 = np.array((point2[0], point2[1], point2[2]))
        euclidean = np.linalg.norm(dist1 - dist2)
        if sum > segmentPoint:
            break
        sum += euclidean
        stopIndex = i

    segmentedPoints = points[:stopIndex+1].copy()

    return segmentedPoints , timestamp[:stopIndex+1].copy()

def plot(segmentedPoints, timestamps, choice = 0):
    if choice == 0:
        plt.plot(segmentedPoints, timestamps, label='segmented Points')
    elif choice ==1:
        plt.scatter(segmentedPoints, timestamps, label='segmented Points')
    else:
        plt.plot(segmentedPoints, timestamps, label='segmented Points')
        plt.scatter(segmentedPoints, timestamps, label='segmented Points')
    plt.legend()
    plt.show()






print("===========================test file==============================")
segmentedPoints, timestamps = get_segmented_points_by_Euclidean("testing/dribbling walking  v zigag pass_6535344602994.txt", True)
# print("total euclidean",total_euclidean)
plot(timestamps,segmentedPoints)



