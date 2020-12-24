# https://www.curiousily.com/posts/time-series-classification-for-human-activity-recognition-with-lstms-in-keras/

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # so the code does not run on CPU

#Load libraries
from tensorflow.python.keras.layers import Dropout, Bidirectional, LSTM, Dense
from scipy.stats import stats
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from tensorflow.python.keras.models import Sequential
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib
from tensorflow.python.keras.models import load_model
from datetime import datetime
import zope.interface
import IClassification

@zope.interface.implementer(IClassification.IClassification)
class RNN():

    def CreatModel(self):
        plt.style.use('fivethirtyeight')

        column_names = ['handRightX', 'handRightY', 'handRightZ',
          'ElbowRightX', 'ElbowRightY', 'ElbowRightZ',
          'ShoulderRightX', 'ShoulderRightY', 'ShoulderRightZ',
          'HipLeftX', 'HipLeftY', 'HipLeftZ',
          'HipRightX', 'HipRightY', 'HipRightZ',
          'label'
        ]

        #Store the data set
        df = pd.read_csv("dataset.csv", header=None, names=column_names)

        row_count = len(df.index)
        train_row = row_count * 0.7

        #-------------
        df_train = df[df.index <= train_row]
        df_test = df[df.index > train_row]

        scale_columns = [
          'handRightX', 'handRightY', 'handRightZ',
          'ElbowRightX', 'ElbowRightY', 'ElbowRightZ',
          'ShoulderRightX', 'ShoulderRightY', 'ShoulderRightZ',
          'HipLeftX','HipLeftY', 'HipLeftZ',
          'HipRightX', 'HipRightY', 'HipRightZ'
          ]

        scaler = RobustScaler()
        scaler = scaler.fit(df_train[scale_columns])

        df_train.loc[:, scale_columns] = scaler.transform(
          df_train[scale_columns].to_numpy()
        )

        df_test.loc[:, scale_columns] = scaler.transform(
          df_test[scale_columns].to_numpy()
        )

        def create_dataset(X, y, time_steps=1, step=1):
             Xs, ys = [], []
             for i in range(0, len(X) - time_steps, step):
                 v = X.iloc[i:(i + time_steps)].values
                 labels = y.iloc[i: i + time_steps]
                 Xs.append(v)
                 ys.append(stats.mode(labels)[0][0])
             return np.array(Xs), np.array(ys).reshape(-1, 1)

        STEP = 10 # ????????

        X_train, y_train = create_dataset(
            df_train[['handRightX','handRightY','handRightZ','ElbowRightX','ElbowRightY','ElbowRightZ','ShoulderRightX','ShoulderRightY','ShoulderRightZ','HipLeftX','HipLeftY','HipLeftZ','HipRightX','HipRightY','HipRightZ']],
            df_train.label,
            95, # ???????????
            STEP
        )

        X_test, y_test = create_dataset(
            df_test[['handRightX','handRightY','handRightZ','ElbowRightX','ElbowRightY','ElbowRightZ','ShoulderRightX','ShoulderRightY','ShoulderRightZ','HipLeftX','HipLeftY','HipLeftZ','HipRightX','HipRightY','HipRightZ']],
            df_test.label,
            40,  # ??????????????????
            STEP
        )

        # change string to value
        enc = OneHotEncoder(handle_unknown='ignore', sparse=False)
        enc = enc.fit(y_train)
        y_train = enc.transform(y_train)
        y_test = enc.transform(y_test)

        #-------------

        model = Sequential()
        model.add(
            Bidirectional(
              LSTM(
                  units=128,
                  input_shape=[X_train.shape[1], X_train.shape[2]]
              )
            )
        )
        model.add(Dropout(rate=0.5))
        model.add(Dense(units=128, activation='relu'))
        model.add(Dense(y_train.shape[1], activation='softmax'))

        model.compile(optimizer='sgd',
                      loss='binary_crossentropy',
                      metrics=['acc'])

        history = model.fit(
                X_train, y_train,
                epochs=20,
                batch_size=32,
                validation_split=0.1,
                shuffle=False
            )

        model.evaluate(X_test, y_test)

        # save the model to disk
        # creates a HDF5 file
        model.save('RNN_model.h5')

    def RunModel(self,y_test):
        # returns a compiled model
        # identical to the previous one

        model = load_model('RNN_model.h5')
        result = model.evaluate(self.X_test, y_test)


        return result

    def Classify(self, arraySignals):
        return self.RunModel(arraySignals)