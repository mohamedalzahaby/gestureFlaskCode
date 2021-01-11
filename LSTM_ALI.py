from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd


def segment(arr, bucket_size=50, overlap_count=0):
    arr_len = len(arr)
    windows = []
    for i in range(0, arr_len - bucket_size + 1, bucket_size - overlap_count):
        window_data = arr[i:i + bucket_size]
        windows.append(window_data)
    return windows


def decode(arr):
    dec = {0: 'walking', 1: 'zigzag', 2: 'dribbling', 3: 'pass', 4: 'v'}
    return [dec[element] for element in arr]


def pad_with_last(arr, pad_len=760):
    indices = []
    seg_len = len(arr)
    num_rows = pad_len - seg_len
    padded_arr = arr + num_rows * [arr[-1]]
    return padded_arr


def pred_lstm(path):
    filepath = './saved_model'
    model = load_model(filepath, compile=True)

    temp_df = pd.read_table(path, delimiter=',', names=('t', 'acc_x', 'acc_y', 'acc_z'))
    arr = np.array(temp_df[['acc_x', 'acc_y', 'acc_z']]).tolist()

    padded_windows = []
    windows = segment(arr)
    for window in windows:
        padded_windows.append(pad_with_last(window))

    preds = np.argmax(model.predict(padded_windows), axis=1)
    # preds = model.predict(padded_windows)
    # return decode(preds)
    return decode(preds)