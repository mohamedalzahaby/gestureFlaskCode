from bunch import bunchify
from scipy.spatial.distance import euclidean
import json
import numpy as np
from fastdtw import fastdtw
from algorithms.Segmenter import split_arrays


class FastDtwController:

    def __init__(self):
        self.classNames = ["walking", "dribbling", "right_pass", "right_v", "walking", "wrong_pass_1", "wrong_pass_2"]


    def writeDataset(self, dataset):
        dict__ = dataset.__dict__
        json_object = json.dumps(dict__)
        # Writing to Dataset.json
        with open("Dataset.json", "w") as outfile:
            outfile.write(json_object)


    # Python program to read JSON
    # from a file
    # Opening JSON file
    def readDataset(self):
        with open('../Dataset.json', 'r') as openfile:
            # Reading from json file
            dictt = json.load(openfile)

        # dataset = Dataset()
        self.dataset = bunchify(dictt)
        self.classes = [self.dataset.walking, self.dataset.dribbling, self.dataset.right_pass, self.dataset.right_v,
                   self.dataset.walking, self.dataset.wrong_pass_1, self.dataset.wrong_pass_2]
        return self.dataset

    def predict(self, testMovePointsList):
        # print(self.dataset.walking[0].accelerometer.points[0].x)
        min = np.inf
        for i, singleClass in enumerate(self.classes):
            for move in singleClass:
                pointsList = []
                for point in move.accelerometer.points:
                    pointsList.append([point.x, point.y, point.z])
                distance, path = fastdtw(testMovePointsList, pointsList, dist=euclidean)

                if min > distance:
                    min = distance
                    result = self.classNames[i]
                    print(f"min = {min}, result = {result}")
                # if result == self.classNames[-1]:
                #     return self.classNames[i]
                if min == 0.0:
                    return result
        return result


    def predictAll(self , testFileMoves):
        results = []
        for i,move in enumerate(testFileMoves):
            print(f"================ move {i+1} ================")
            results.append(self.predict(move))
        return results

    # def predictFile(self , path):
    #     moves = segment(path)
    #     print("len(moves)",len(moves))
    #     results = self.predictAll(moves)
    #     return results

    def predictFile(self , textFileName):
        points = self.get_points(textFileName)
        moves = np.array_split(points, 10)
        result = self.predictAll(moves)
        return result


    def get_points(self, textFileName):
        timestamp, x, y, z = split_arrays(textFileName)
        points = []
        for i in range(len(timestamp)):
            point = [x[i], y[i], z[i]]
            points.append(point)
        return points





