from os import listdir
from os.path import isfile, join
from Segmenter import segment
from Recogniser import get_xyz_of_move, getMagnitude, createArray, getRecognizer, get_all_moves_in_all_dirs

def getResult(filePath, recognizer):
    testingFileMoves = segment(filePath)
    print("len(testingFileMoves)", len(testingFileMoves))
    for move in testingFileMoves:
        x, y, z = get_xyz_of_move(move)
        Magnitude = getMagnitude(x, y)
        inputArray = createArray(Magnitude, z)
        # print("length of inputArray = ", len(inputArray))
        result = recognizer.recognize(inputArray, 5)
        # return result
        print(result)

def getRangeOf_n_Results(length, inputArray, recognizer):
    for i in range(length):
        if i%5 == 0 and i != 0:
            result = recognizer.recognize(inputArray,i)
            print("n = ",i," result = ",result)

def runAllTestFiles():
    path = "new dataset/"
    dirNames = ["pass","v", "zigzag", "dribbling"]
    allDirsMoves = get_all_moves_in_all_dirs(path, dirNames)
    recognizer = getRecognizer(allDirsMoves, dirNames)
    testingFiles = [f for f in listdir("testing") if isfile(join("testing", f))]
    # print(testingFiles)
    for file in testingFiles:
        result = getResult("testing/" + file, recognizer)
        print("result = ", result)
        # getRangeOf_n_Results(205, inputArray)

def runSingleFile(file):
    path = "new dataset/"
    dirNames = ["pass","v", "dribbling"]
    allDirsMoves = get_all_moves_in_all_dirs(path, dirNames)
    recognizer = getRecognizer(allDirsMoves, dirNames)
    getResult(file, recognizer)
    # print("result = ", result)
    # return result

#################### MAIN HERE ####################
runAllTestFiles()
# runSingleFile("testing/pass_54566035684797.txt")
# print(result)