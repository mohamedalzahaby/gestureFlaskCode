from os import listdir
from os.path import isfile, join
from qdollar.recognizer import Gesture,Recognizer, Point
from Recogniser import getTemplates, get_all_moves_in_all_dirs, get_xyz_of_move, getMagnitude
from Segmenter import segment
#################################################################### example start ####################################################################
# # points
# points1 = [ Point(0, 0, 1), Point(1, 1, 1), Point(0, 1, 2), Point(1, 0, 2)]
# points2 = [Point(0, 0), Point(1, 0)]
# testPoints = [Point(31, 141, 1), Point(109, 222, 1), Point(22, 219, 2), Point(113, 146, 2)]
#
# # templates
# tmpl_1 = Gesture('X', points1)
# tmpl_2 = Gesture('line', points2)
# gesture = Gesture('A', testPoints)
#
# templates = [ tmpl_1, tmpl_2]
#
# # recognise
# result , score= Recognizer().classify(gesture, templates)
# # print(len(result))
# print("score =",score)
# print("result =",result.name)
#
# for point in result.Points:
#     print("strokeId =", point.strokeId, "x =", point.x, "y =", point.y, "intX =", point.intX, "intY =", point.intY)
#     print("=======================================================================================")
#################################################################### example End ####################################################################


# res = Recognizer().classify(gesture, templates)
# print(res[0].name)



def getResults(file, templates):
    results = []
    testingFileMoves = segment(file, True)
    print("number of Moves in test File ", len(testingFileMoves))
    for move in testingFileMoves:
        x, y, z = get_xyz_of_move(move)
        Magnitude = getMagnitude(x, y)
        points = getPoints(Magnitude, z)
        gesture = Gesture('testFile', points)
        result = Recognizer().classify(gesture, templates)
        results.append(result)
    return results


def getPoints(magnitude, z, numberOfStrokes = 1):
    # print(len(magnitude))
    points = []
    for i in range(len(magnitude)):
        point = Point(magnitude[i], z[i], numberOfStrokes)
        points.append(point)
    return points

def getTemplates(all_moves_in_all_dirs, dirNames):
    Templates = []
    for i in range(len(all_moves_in_all_dirs)):
        all_moves_in_one_dir = all_moves_in_all_dirs[i]
        dirTemplates = getTemplatesInDirectory(all_moves_in_one_dir, dirNames[i])
        Templates.extend(dirTemplates)
    return Templates

def getTemplatesInDirectory(all_moves_in_one_dir, dirName):
    Templates = []
    for i in range(len(all_moves_in_one_dir)):
        fileMoves = all_moves_in_one_dir[i]
        for move in fileMoves:
            x, y, z = get_xyz_of_move(move)
            magnitude = getMagnitude(x, y)
            points = getPoints(magnitude, z)
            template = Gesture(dirName, points)
            Templates.append(template)
    return Templates

def runAllTestFiles():
    path = "new dataset/"
    dirNames = ["pass","v", "zigzag", "dribbling"]
    testFiles = [f for f in listdir("testing") if isfile(join("testing", f))]
    # print(testFiles)
    for file in testFiles:
        print(file)
        runSingleFile("testing/"+file)
        print("=============================")


def runSingleFile(file):
    path = "new dataset/"
    dirNames = ["pass","v", "dribbling"]
    all_moves_in_all_dirs = get_all_moves_in_all_dirs(path, dirNames)
    templates = getTemplates(all_moves_in_all_dirs, dirNames)
    # print(res[0].name)
    # recognise
    results = getResults(file, templates)
    for resultData in results:
        result , score= resultData
        print("score =",score)
        print("result =", result.name)
        # for point in result.Points:
        #     print("strokeId =", point.strokeId, "x =", point.x, "y =", point.y, "intX =", point.intX, "intY =", point.intY)
        #     print("=======================================================================================")

runSingleFile("testing/v_23871390355108.txt")
# runAllTestFiles()

# dataset = []
# root = "new dataset/"
# dirNames = ["pass","v", "zigzag", "dribbling"]
# for dirName in dirNames:
#     trainingMoves = []
#     testingMoves = []
#     dir = listdir(root + dirName)
#     end = int(len(dir) * 0.7 + 1)
#     trainingFiles , testingFiles  = dir[:end] , dir[end:]
#     [trainingMoves.append(segment(root+dirName+'/'+file)) for file in trainingFiles]
#     [testingMoves.append(segment(root+dirName+'/'+file)) for file in trainingFiles]
#     tuple = (dirName , trainingMoves, testingMoves)
#     dataset.append(tuple)
#     print(dataset)
#     break



# for tuple in dataset:
#     trainingMoves = tuple[1]
#     testingMoves  = tuple[2]
#     for file in trainingMoves:
#         move = segment(file)
#         trainingMoves.append(move)



















