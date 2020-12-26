from dollarpy import Recognizer, Template, Point
from os import listdir
from os.path import isfile, join
from Segmenter import segment
import math


# magnitude of xy
def getMagnitude(x, y):
    xyMagnitudes = []
    for i in range(len(x)):
        magnitude = math.sqrt(math.pow(x[i], 2) + math.pow(y[i], 2))
        xyMagnitudes.append(magnitude)
    return xyMagnitudes


def getPoints(magnitude, z, numberOfStrokes = 1):
    # print(len(magnitude))
    points = []
    for i in range(len(magnitude)):
        point = Point(magnitude[i], z[i], numberOfStrokes)
        points.append(point)
    return points

def getPointsWithoutStrokes(magnitude, z):
    points = []
    for i in range(len(magnitude)):
        point = [magnitude[i], z[i]]
        points.append(point)
    return points

def getPointsWithxyz(x, y, z):
    points = []
    for i in range(len(x)):
        point = [x[i], y[i], z[i]]
        points.append(point)
    return points


def getRecognizer(all_moves_in_all_dirs, dirNames):
    Templates = getTemplates(all_moves_in_all_dirs, dirNames)
    return Recognizer(Templates)

# go through every directory and get its templates to return dribbling_pass_v_zigzag template
def getTemplates(all_moves_in_all_dirs, dirNames):
    Templates = []
    for i in range(len(all_moves_in_all_dirs)):
        all_moves_in_one_dir = all_moves_in_all_dirs[i]
        dirTemplates = getTemplatesInDirectory(all_moves_in_one_dir, dirNames[i])
        Templates.extend(dirTemplates)
    return Templates


def getTemplatesInDirectory(dirMoves, dirName):
    Templates = []
    for i in range(len(dirMoves)):
        fileMoves = dirMoves[i]
        for move in fileMoves:
            x, y, z = get_xyz_of_move(move)
            magnitude = getMagnitude(x, y)
            points = getPoints(magnitude, z)
            template = Template(dirName, points)
            # if i == 0:
            #     # print("points = ", type(points[0]))
            #     print("template points = ",template[0].x)
            Templates.append(template)
    return Templates


def get_xyz_of_move(move):
    x, y, z = [], [], []
    for i in range(len(move)):
        x.append(move[i][0])
        y.append(move[i][1])
        z.append(move[i][2])
    return x, y, z



def get_all_moves_in_dir(mypath, dirName):
    all_moves_in_dir = []
    files = [f for f in listdir(mypath + dirName) if isfile(join(mypath + dirName, f))]
    for fileName in files:
        all_moves_in_file = segment(mypath + dirName + "/" + fileName)
        all_moves_in_dir.append(all_moves_in_file)
        # print("number of moves in file = ", len(all_moves_in_file))
    return all_moves_in_dir

def get_all_moves_in_all_dirs(mypath, allDirNames):
    all_moves_in_all_dirs = []
    for dirName in allDirNames:
        all_moves_in_dir = get_all_moves_in_dir(mypath, dirName)
        all_moves_in_all_dirs.append(all_moves_in_dir)
    return all_moves_in_all_dirs



# all_moves_in_all_dirs array(
#                               all_moves_in_dirarray(
#                                                       all_moves_in_file array(
#                                                                                  moves
#                                                                                  moves
#                                                                               )
#                                                       all_moves_in_file array()
#                                                    )
#                               all_moves_in_dirarray()
#                            )

