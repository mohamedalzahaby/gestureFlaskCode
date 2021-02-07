from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import matplotlib.pyplot as plt
# from Controllers.FastDtwController import FastDtwController
from algorithms.Segmenter import split_arrays, getMagnitudes

pess_temp1 = "dataset/u1/right pass/2/a2.txt"
v_temp1 = "dataset/u1/right v/2/a2.txt"

def get_points(textFileName):
    timestamp, x, y, z = split_arrays(textFileName)
    points = []
    for i in range(len(timestamp)):
        point = [x[i], y[i], z[i]]
        points.append(point)
    return points

def get_segmented_points(magnitudes, x, y, z):
    points = []
    for magnitude in magnitudes:
        index = magnitudes.index(magnitude)
        points.append([x[index], y[index], z[index]])
    return points

def get_temp(pess_temp1, i, j, plotting = False):
    pass_timestamp, pass_x, pass_y, pass_z = split_arrays(pess_temp1)
    pass_magnitudes = getMagnitudes(pass_x, pass_y, pass_z)
    points = get_segmented_points(pass_magnitudes, pass_x, pass_y, pass_z)
    if plotting:
        plt.plot(pass_magnitudes[i:j])
        plt.show()

    dataframe_correct_temp1 = pass_magnitudes[i:j].copy()
    return dataframe_correct_temp1, points[i:j].copy()

dataframe_correct_pass_temp1, pass_points = get_temp(pess_temp1, 0, -1)
dataframe_correct_v_temp1, v_points = get_temp(v_temp1,0,-1)

first_try = "testFiles/a_5v_5pass_sec-try_98015637128908_accelerometer.txt"

start = 200
const = 300
end = start + const
timestamp, x, y, z = split_arrays(first_try)
magnitudes = getMagnitudes(x, y, z)
test_file_points = get_points(first_try)

while(end < len(test_file_points)-const):

    dataframe = magnitudes[start:end]
    # plt.plot(dataframe)
    # plt.plot(dataframe_correct_v_temp1)
    # plt.plot(dataframe_correct_pass_temp1)
    # plt.show()
    pass_distance, pass_path = fastdtw(dataframe_correct_pass_temp1, dataframe, dist=euclidean)
    v_distance, vpath = fastdtw(dataframe_correct_v_temp1, dataframe, dist=euclidean)
    if (pass_distance < v_distance):
        print(f"pass = {int(pass_distance)}")
    else:
        print(f"v = {int(v_distance)}")
    start = end - 50
    end = start + const