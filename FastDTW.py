from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from Recogniser import get_xyz_of_move, getMagnitude, getPointsWithoutStrokes, getPointsWithxyz, getRecognizer, \
    get_all_moves_in_all_dirs
from Segmenter import segment
import numpy as np

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
#                               all_moves_in_dirarray(
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
    recognizer = getRecognizer(allDirsMoves, dirNames)
    # results = get_FastDtw_Results_through_magnitude(file, recognizer)
    results = get_FastDtw_Results_through_xyz(file, allDirsMoves, dirNames)
    print(results)

