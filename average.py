from Segmenter import split_arrays
import statistics
from os import listdir
from os.path import isfile, join
def runAllTestFiles():
    path = "new dataset/"
    dirNames = ["pass","v", "zigzag", "dribbling"]
    all_timestamp_in_all_dirs = get_all_timestamp_in_all_dirs(path, dirNames)
    for all_timestamp_in_dir in all_timestamp_in_all_dirs:
        dirsDuration = []
        for timestamps_in_file in  all_timestamp_in_dir:
            start = timestamps_in_file[0]
            end = timestamps_in_file[-1]
            duration = end - start
            duration = duration/1000000000
            dirsDuration.append(duration)
        avg = statistics.mean(dirsDuration)

    avg = (3.8437194824 + 3.0914062499 + 5.474634344090909 + 4.5027648926)/4
    print("avg=",avg)





def get_all_timestamp_in_dir(mypath, dirName):
    all_timestamp_in_dir = []
    files = [f for f in listdir(mypath + dirName) if isfile(join(mypath + dirName, f))]
    for fileName in files:
        # print(fileName)
        timestamp, x, y, z = split_arrays(mypath + dirName + "/" + fileName)
        all_timestamp_in_dir.append(timestamp)
    return all_timestamp_in_dir

def get_all_timestamp_in_all_dirs(mypath, allDirNames):
    all_timestamps_in_all_dirs = []
    for dirName in allDirNames:

        all_timestamps_in_dir = get_all_timestamp_in_dir(mypath, dirName)
        all_timestamps_in_all_dirs.append(all_timestamps_in_dir)
    return all_timestamps_in_all_dirs



runAllTestFiles()