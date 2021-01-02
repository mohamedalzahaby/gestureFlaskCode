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


def getEuclidean(file, plot=False):
    # print("=================================",file,"=================================")
    # moves = segment(file, plot)
    timestamp, x, y, z = split_arrays(file)
    # magnitudes = getMagnitudes(x, y, z)
    # modes = []
    # for t in timestamp:
    #     modes.append(1)
    #
    # plt.switch_backend('TkAgg')  # TkAgg (instead Qt4Agg)
    # fig, axs = plt.subplots(2)
    # fig.suptitle('segmentation')
    # mng = plt.get_current_fig_manager()
    # ## works on Ubuntu??? >> did NOT working on windows
    # mng.resize(*mng.window.maxsize())
    # mng.window.state('zoomed')  # works fine on Windows!
    # # np.array()
    # plotMovingAverageWithThreshold(timestamp, modes, magnitudes, axs[1])
    # plt.show()


    # print("number of t = ",len(timestamp))
    points = get_points(timestamp, x, y, z)
    # print("len(moves)",len(points))
    euclideans = []
    for i in range(len(points)-1):
        distance = points
        point1 = points[i]
        point2 = points[i + 1]
        dist1 = np.array((point1[0], point1[1], point1[2]))
        dist2 = np.array((point2[0], point2[1], point2[2]))
        euclidean = np.linalg.norm(dist1 - dist2)
        # print(euclidean)
        euclideans.append(euclidean)

    avg  = statistics.mean(euclideans)
    euclideans.sort()
    Max = euclideans[-1]
    Min = euclideans[0]
    mode = max(set(euclideans), key=euclideans.count)
    # if plot:

    # print("avg =",avg,"mode =",mode,"max =",Max,"min =",Min, "sum of euclideans =", int(sum(euclideans)))
    # print( "sum of euclideans =", int(sum(euclideans)))
    return sum(euclideans)

def runAllTestFiles():
    path = "new dataset/"
    dirNames = ["pass","v", "dribbling", "zigzag", "walking"]
    avgs = 0
    modes = 0
    for dir in dirNames:
        print(dir)
        files = [f for f in listdir(path + dir) if isfile(join(path + dir, f))]
        total_euclideans = []
        for fileName in files:
            total_euclideans.append(getEuclidean(path + dir +"/"+fileName))
            avg = statistics.mean(total_euclideans)
            total_euclideans.sort()
            Max = int(total_euclideans[-1])
            Min = int(total_euclideans[0])
            mode = int(max(set(total_euclideans), key=total_euclideans.count))
        print("avg =",int(avg),"mode =",mode,"max =",Max,"min =",Min)
        avgs += avg
        modes += mode
    print("total avgs=",int(avgs), "total modes=",int(modes))


runAllTestFiles()
print("===========================test file==============================")
total_euclidean = getEuclidean("testing/dribbling walking  v zigag pass_6535344602994.txt",True)
print("total euclidean",total_euclidean)





# v          27
# dribbling  63
# zigzag     90
# pass       101
# walking    208