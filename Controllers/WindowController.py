import numpy as np
from algorithms.Segmenter import split_arrays

class WindowController:

    def get_points(self, x, y, z):
        points = []
        for i, axis in enumerate(x):
            point = [x[i], y[i], z[i]]
            points.append(point)
        return points

    def get_euclidean_window(self, points):
        euclideans = []
        for i, point in enumerate(points, 1):
            point1 = points[i - 1]
            point2 = point
            euclidean = self.calculate_eculidean(point1, point2)
            euclideans.append(euclidean)
        return euclideans

    def get_euclidean_windows(self, points, windowSize=21):
        windows = []
        for i, point in enumerate(points):
            part = points[i: i + windowSize]
            window = self.get_euclidean_window(part)
            windows.append(window)
        return windows

    def get_file_Euclidean_Windows(self, file, windowSize=21):
        windows = []
        timestamp, x, y, z = split_arrays(file)
        points = self.get_points(x, y, z)
        self.get_euclidean_windows(points, windowSize)
        return windows

    def calculate_eculidean(self, point1, point2):
        dist1 = np.array((point1[0], point1[1], point1[2]))
        dist2 = np.array((point2[0], point2[1], point2[2]))
        euclidean = np.linalg.norm(dist1 - dist2)
        return euclidean