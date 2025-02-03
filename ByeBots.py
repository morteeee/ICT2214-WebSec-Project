import torch
import torch.nn as nn
import joblib
import numpy as np
import pandas as pd
import json
from flask import jsonify

class Autoencoder(nn.Module):
    def __init__(self, input_dim):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4)
        )
        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class ByeBots:
    def __init__(self):
        self.scalar = joblib.load('models/9.pkl')
        self.inputSize = 8
        self.model = Autoencoder(self.inputSize)
        self.model.load_state_dict(torch.load("models/9.pth"))
        self.model.eval()

        # Model 7 (SECOND BEST)
        # self.min_error = 2.1803902e-05
        # self.threshold = 0.005876108631491658

        #Model 8 (GARBAGE UNLESS YOU WANT TO USE IT)
        # self.min_error = 4.223479e-05
        # self.threshold = 0.02339418102055788

        #Model 9 (BEST)
        self.min_error = 8.322179e-06
        self.threshold = 0.0037997495033778245



        self.TIME_INTERVAL = 0.15

        self.columns = [
            "path_length", "avg_speed", "acceleration", "jerk", "curvature", "straightness", 
            "jitter", "direction_changes"
        ]
    
    def processData(self, datasetText):
        datasetList = []
        if datasetText != "":
            parsed = json.loads(datasetText)
            datasetList.append(parsed)
        df = pd.DataFrame(datasetList)

        for index, row in df.iterrows():
            dataSplit = row['sensorData'].split(';')[1:len(row['sensorData'].split(';')) - 1]
            df.at[index, 'sensorData'] = dataSplit

        df = df[df['sensorData'].map(lambda x: len(x) > 4)]
        df.reset_index(drop=True, inplace=True)

        for index, row in df.iterrows():
            sensorData = row['sensorData']
            totalMousePoints = 0
            
            x_coords = []
            y_coords = []
            
            for data in sensorData:
                if 'scroll' in data:
                    pass
                elif 'click' in data:
                    pass
                elif 'key' in data:
                    pass
                else:
                    try:
                        mouseAtX, mouseAtY = data.split('-')
                        x_coords.append(int(mouseAtX))
                        y_coords.append(int(mouseAtY))
                        totalMousePoints += 1
                    except ValueError:
                        continue

            df.at[index, 'totalMousePoints'] = totalMousePoints
            df.at[index, 'x_coords'] = json.dumps(x_coords)
            df.at[index, 'y_coords'] = json.dumps(y_coords)

        return df
        
    def compute_curvature(self, x_coords, y_coords, time_interval=0.15):
        x_coords = np.array(x_coords, dtype=float)
        y_coords = np.array(y_coords, dtype=float)
        
        dx = np.diff(x_coords)
        dy = np.diff(y_coords)
        
        distances = np.sqrt(dx ** 2 + dy ** 2)
        angles = np.arctan2(dy, dx)
        angles = np.unwrap(angles)
        delta_angles = np.diff(angles)

        if len(distances) < 2:
            return 0
        
        avg_lengths = (distances[:-1] + distances[1:]) / 2.0 + 1e-6
        
        curvatures = np.abs(delta_angles) / avg_lengths
        
        mean_curvature = np.mean(curvatures)
        
        return mean_curvature

    def calculate_features(self, df):
        new_features = {
            "path_length": [],
            "avg_speed": [],
            "acceleration": [],
            "jerk": [],
            "curvature": [],
            "straightness": [],
            "idle_time_count": [],
            "jitter": [],
            "direction_changes": []
        }

        for index, row in df.iterrows():
            x_coords = np.array(json.loads(row['x_coords']))
            y_coords = np.array(json.loads(row['y_coords']))

            if len(x_coords) < 2:
                for key in new_features:
                    new_features[key].append(0)
                continue

            distances = np.sqrt(np.diff(x_coords) ** 2 + np.diff(y_coords) ** 2)
            total_distance = np.sum(distances)
            speeds = distances / self.TIME_INTERVAL
            avg_speed = np.mean(speeds) if len(speeds) > 0 else 0
            accelerations = np.diff(speeds) / self.TIME_INTERVAL
            avg_acceleration = np.mean(accelerations) if len(accelerations) > 0 else 0
            jerks = np.diff(accelerations) / self.TIME_INTERVAL
            avg_jerk = np.mean(jerks) if len(jerks) > 0 else 0


            curvature = self.compute_curvature(x_coords, y_coords, self.TIME_INTERVAL)

            straight_line_distance = np.linalg.norm([x_coords[-1] - x_coords[0], y_coords[-1] - y_coords[0]])
            straightness = total_distance / (straight_line_distance + 1e-6)

            idle_time_count = np.sum((x_coords[:-1] == x_coords[1:]) & (y_coords[:-1] == y_coords[1:]))

            jitter = np.std(distances) if len(distances) > 1 else 0

            angles = np.arctan2(np.diff(y_coords), np.diff(x_coords))
            angles = np.unwrap(angles)
            direction_changes = np.sum(np.abs(np.diff(angles)) > np.pi / 4)

            new_features["path_length"].append(total_distance)
            new_features["avg_speed"].append(avg_speed)
            new_features["acceleration"].append(avg_acceleration)
            new_features["jerk"].append(avg_jerk)
            new_features["curvature"].append(curvature)
            new_features["straightness"].append(straightness)
            new_features["idle_time_count"].append(idle_time_count)
            new_features["jitter"].append(jitter)
            new_features["direction_changes"].append(direction_changes)

        for key, values in new_features.items():
            df[key] = values

        return df

    def finalCleaning(self, df):
        df.drop(columns=['userAgent', 'language', 'platform', 
                    'deviceMemory', 'doNotTrack', 
                   'screenResolution', 'colorDepth', 'plugins', 
                 'mimeTypes', 'timezoneOffset',
                'hardwareConcurrency', 'touchSupport', 'webdriver', 'viewportWidth', 'viewportHeight', 'sensorData'], inplace=True)

        # df = df[df['totalMousePoints'] >= 10]

        df = df.reset_index(drop=True)

        df = self.calculate_features(df)

        df.drop(columns=['idle_time_count', 'x_coords', 'y_coords'], inplace=True)

        df = df.drop(columns=["totalMousePoints"])

        df = df.reset_index(drop=True)

        return df

    # def validateFingerprint(self, rawFingerprint):
    #     df = self.processData(rawFingerprint)

    #     if len(df.values.tolist()) == 0:
    #         return 0.0

    #     df = self.finalCleaning(df)
    #     sample = np.array(df.values.tolist())

    #     print("Curvature:", df.values.tolist()[0][-4])

    #     new_data_scaled = self.scalar.transform(sample.reshape(1, -1))
    #     new_data_tensor = torch.tensor(new_data_scaled, dtype=torch.float32)
        
    #     with torch.no_grad():
    #         reconstructed = self.model(new_data_tensor)
    #         loss = torch.mean((new_data_tensor - reconstructed) ** 2).item()
        
    #     confidence = 100 * (1 - (loss - self.min_error) / (self.threshold - self.min_error))
    #     confidence = np.clip(confidence, 0, 100)

    #     return confidence

    def validateFingerprint(self, rawFingerprint):
        df = self.processData(rawFingerprint)

        if len(df.values.tolist()) == 0:
            return 0.0

        df = self.finalCleaning(df)
        sample = np.array(df.values.tolist())

        # For debugging: print one of the features (e.g., curvature)
        # print("Curvature:", df.values.tolist()[0][-4])

        new_data_scaled = self.scalar.transform(sample.reshape(1, -1))
        new_data_tensor = torch.tensor(new_data_scaled, dtype=torch.float32)
        
        with torch.no_grad():
            reconstructed = self.model(new_data_tensor)
            
            errors = (new_data_tensor - reconstructed) ** 2
            
            overall_loss = torch.mean(errors).item()
            confidence_overall = 100 * (1 - (overall_loss - self.min_error) / (self.threshold - self.min_error))
            confidence_overall = np.clip(confidence_overall, 0, 100)
            
            feature_errors = errors[0].cpu().numpy()
            confidence_per_feature = 100 * (1 - (feature_errors - self.min_error) / (self.threshold - self.min_error))
            confidence_per_feature = np.clip(confidence_per_feature, 0, 100)
        

        featureConfidence = {

        }
        print("")
        print("Overall Confidence:", confidence_overall)
        for i, conf in enumerate(confidence_per_feature):
            print(f"Feature {self.columns[i]} Confidence: {conf}")
            featureConfidence[self.columns[i]] = float(conf)
        print("")
        return featureConfidence
