from os import listdir
from os.path import isfile, join
from Segmenter import segment
from Recogniser import get_xyz_of_move, getMagnitude, createArray, getRecognizer, getAllDirS_moves


path = "new dataset/"
dirNames = ["pass","v", "zigzag", "dribbling"]
allDirsMoves = getAllDirS_moves(path, dirNames)
recognizer = getRecognizer(allDirsMoves, dirNames)
testingFiles = files = [f for f in listdir("testing") if isfile(join("testing", f))]
# print(testingFiles)
for file in testingFiles:
    print(file)
    testingFileMoves = segment("testing/"+file)
    print("number of moves = ", len(testingFileMoves))

    for move in testingFileMoves:
        x, y, z = get_xyz_of_move(move)
        Magnitude = getMagnitude(x, y)
        inputArray = createArray(Magnitude, z)
        print("length of inputArray = ", len(inputArray))
        result = recognizer.recognize(inputArray, 5)
        print("result = ",result)
        # getRangeOf_n_Results(205, inputArray)


def getRangeOf_n_Results(length, inputArray):
    for i in range(length):
        if i%5 == 0 and i != 0:
            result = recognizer.recognize(inputArray,i)
            print("n = ",i," result = ",result)