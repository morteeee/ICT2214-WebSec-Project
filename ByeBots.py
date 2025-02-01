import os
import warnings
from sklearn.exceptions import InconsistentVersionWarning
import absl.logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
absl.logging.set_verbosity(absl.logging.ERROR)
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

import numpy as np
import pandas as pd
import json
import numpy as np
import numpy as np
import joblib
from keras.models import load_model
from keras.losses import MeanSquaredError
import time
import math

from CurveScore import CurveScore


class ByeBots:
    def __init__(self):
        self._CurveScore = CurveScore()
        
        self._df = None

        self._h5dnModelPath = "models/3.h5"
        self._scalerPickelPath = "models/scaler3.pkl"

        self._autoencoder, self._scaler = self.loadModel()

        self._MODEL_THRESHOLD = 0.70

        
    
    def loadModel(self):
        scaler = joblib.load(self._scalerPickelPath)
        autoencoder = load_model(
            self._h5dnModelPath,
            custom_objects={'mse': MeanSquaredError()}
        )

        return autoencoder, scaler


    def preprocessFingerprint(self, fingerprintString):
        datasetList = []
        if fingerprintString != "":
            parsed = json.loads(fingerprintString)
            datasetList.append(parsed)
        df = pd.DataFrame(datasetList)

        for index, row in df.iterrows():
            dataSplit = row['sensorData'].split(';')[1:len(row['sensorData'].split(';')) - 1]
            df.at[index, 'sensorData'] = dataSplit

        for index, row in df.iterrows():
            sensorData = row['sensorData']
            totalClicks = 0
            totalScrolls = 0
            totalKeyPresses = 0
            totalMousePoints = 0
            x_coords = []
            y_coords = []
            
            for data in sensorData:
                if 'scroll' in data:
                    totalScrolls += 1
                elif 'click' in data:
                    totalClicks += 1
                elif 'key' in data:
                    totalKeyPresses += 1
                else:
                    try:
                        mouseAtX, mouseAtY = data.split('-')
                        x_coords.append(int(mouseAtX))
                        y_coords.append(int(mouseAtY))
                        totalMousePoints += 1
                    except ValueError:
                        continue

            df.at[index, 'totalMousePoints'] = totalMousePoints
            df.at[index, 'totalClicks'] = totalClicks
            df.at[index, 'totalScrolls'] = totalScrolls
            df.at[index, 'totalKeyPresses'] = totalKeyPresses
            
            if len(x_coords) > 1:
                df.at[index, 'mouseCurveScore'] = self._CurveScore.curveScore(x_coords, y_coords)
            else:
                df.at[index, 'mouseCurveScore'] = 0
        

        df.drop(columns=['userAgent', 'language', 'platform', 
                    'deviceMemory', 'doNotTrack', 
                   'screenResolution', 'colorDepth', 'plugins', 
                 'mimeTypes', 'timezoneOffset', 'sensorData',
                'hardwareConcurrency', 'touchSupport', 'webdriver'], inplace=True)
        
        self._df = df.copy()
        
    def validateFingerprint(self, fingerprintString, productionMode, selfProvidedDf=None):
        self.preprocessFingerprint(fingerprintString)

        if productionMode:
            new_data_df = self._df
        else:
            new_data_df = pd.DataFrame([selfProvidedDf])
        

        new_data_scaled = self._scaler.transform(new_data_df)
        start_time = time.time()
        reconstructed = self._autoencoder.predict(new_data_scaled, verbose=0)
        end_time = time.time()
        timePSeMS = (end_time - start_time) * 1000
        reconstruction_loss = np.mean(np.square(new_data_scaled - reconstructed), axis=1)
        is_anomaly = reconstruction_loss > self._MODEL_THRESHOLD

        print(reconstruction_loss)

        return {
            "anomaly" : 'Yes' if is_anomaly[0] else 'No',
            "reconstructionLoss" : reconstruction_loss[0],
            "took" : math.floor(float(timePSeMS) * 10000) / 10000
        }


