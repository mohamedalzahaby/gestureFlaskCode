import numpy as np
import matplotlib.pyplot as plt
from Segmenter import split_arrays, getMagnitudes
# importing pandas as pd
import pandas as pd


# Creating the time-series index
def getWindows(whole_df, windowSize = 20):
    dfs, pcts = [], []
    for i in range(0,len(whole_df)-windowSize,10):
        df = whole_df.iloc[i:i+windowSize, :]
        pct = df.pct_change(fill_method='ffill')
        # print(pct)
        dfs.append(df)
        pcts.append(pct)
    return dfs, pcts

# main
def plotme(file):
    timestamp, x, y, z = split_arrays(file)
    magnitudes = getMagnitudes(x, y, z)
    whole_df = pd.DataFrame({"magnitudes": magnitudes}, index=timestamp)
    # whole_df = pd.DataFrame({"magnitudes": magnitudes, "x": x, "y": y, "z": z, }, index=timestamp)
    dfs, pcts = getWindows(whole_df, 20)

    # [print(pct) for pct in pcts]
    # print(abs(pcts[0]["magnitudes"]))

    allPcts = []
    for pct in pcts:
        for magnitude in abs(pct["magnitudes"]):
            allPcts.append(magnitude)

    print('allPcts',allPcts)
    arr = np.arange(len(allPcts))
    threshholdValue = 0.8
    threshold = [threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,threshholdValue,]
    plt.plot(arr,allPcts, label='magnitudes')
    # plt.plot(arr, threshold, label='0.7')
    plt.legend()
    plt.show()


    counters = []
    ctr = 0
    for pct in pcts:
        for magnitude in abs(pct["magnitudes"]):
            if magnitude > threshholdValue:
                ctr += 1
        if ctr != 0:
            counters.append(ctr)
        ctr = 0

    print(counters)
    print(len(counters))

    # arr = np.arange(len(counters))
    # threshholdValue = 0.7
    # plt.plot(arr, counters, label='ctrs')
    # plt.legend()
    # plt.show()


plotme(file="new dataset/v/v_23816079943662.txt")
plotme(file="new dataset/v/v_23882992656480.txt")
plotme(file="new dataset/v/v_23945451632802.txt")
# # plt.plot(timestamp[:20],pct["magnitudes"], label='magnitudes')
# # plt.legend()
# # plt.show()
# magnitudeChangeRate = []
# xChangeRate = []
# yChangeRate = []
# zChangeRate = []
# # for time in timestamp[:20]:
# #     magnitude = pct['magnitudes'].loc[time]
# #     isbigger = ">0.5" if magnitude >= 0.5 else "<0.5"
# #     magnitudeChangeRate.append(isbigger)
# #     x = pct['x'].loc[time]
# #     xChangeRate.append(True if x >= 0.5 else False)
# #     y = pct['y'].loc[time]
# #     yChangeRate.append(True if y >= 0.5 else False)
# #     z = pct['z'].loc[time]
# #     zChangeRate.append(True if z >= 0.5 else False)
#
# pcts  =[]
# for pct in pctList:
#     pcts.extend(pct["magnitudes"].tolist())
#
# print(pctList)
# plt.scatter(timestamp,pcts, label='magnitude change rate')
# plt.legend()
# plt.show()
#
#
#
# # # sma
# # numbers = [1, 2, 3, 7, 9]
# # window_size = 3
# #
# # numbers_series = pd.Series(numbers)
# # windows = numbers_series.rolling(window_size)
# # moving_averages = windows.mean()
# #
# # moving_averages_list = moving_averages.tolist()
# # without_nans = moving_averages_list[window_size - 1:]
# # print("moving_averages_list",moving_averages_list)
# # print(without_nans)
#
#
#
#


















