from os import listdir
from os.path import isfile, join
from PDollar import runAllTestFiles, runSingleFile
from FastDTW import fastDtw

#################### MAIN HERE ####################
# runAllTestFiles()
runSingleFile("testing/v_dribbling_pass_125906839862844.txt")
# fastDtw("testing/v_dribbling_pass_125874054554087.txt")
# print(result)
from Segmenter import segment

# testingFiles = [f for f in listdir("testing") if isfile(join("testing", f))]
# # print(testingFiles)
# for file in testingFiles:
#     print(file)
#     fastDtw("testing/"+file)
#     # print("number of moves filtered =",len(segment("new dataset/zigzag/"+file,True)))
#     print("=============================")



# print("number of moves filtered =",len(segment("new dataset/walking/walking_27234668716293.txt", True)))
# print("number of moves filtered =",len(segment("new dataset/walking/walking_27259381848618.txt", True)))
# print("number of moves filtered =",len(segment("new dataset/walking/walking_27381553268281.txt", True)))
# print("number of moves filtered =",len(segment("new dataset/walking/walking_27438676623692.txt", True)))
# print("number of moves filtered =",len(segment("new dataset/walking/walking_27505023311393.txt", True)))






















