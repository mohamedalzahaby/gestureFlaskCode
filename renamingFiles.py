import os
from os.path import isfile, join
from os import listdir


dirs = "dataset/u2/wrong v 2/"
list = listdir(dirs)
length = len(list)
for i in range(length):
    num = str(i+1)
    files = "dataset/u2/wrong v 2/"+num
    print("files",files)
    for file in listdir(files):
        if file.find("accelerometer") != -1:
            os.rename(r""+files+'/'+file, r""+files+'/a'+num+'.txt')
        if file.find("gyroscope") != -1:
            print("file", file)
            os.rename(r""+files+'/'+file, r""+files+'/g'+num+'.txt')
        print("file", file)
