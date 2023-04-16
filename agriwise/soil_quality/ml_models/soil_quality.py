import numpy
import pickle
import pandas as pd


class Soil_quality_Classifier:
    def __init__(self):
        with open('agriwise/soil_quality/ml_models/random_forest_pkl.pkl', 'rb') as file:
            self.model = pickle.load(file)

    def preprocessing(self, input_data):
        # JSON to pandas DataFrame
        input_data = pd.DataFrame(input_data, index=[0])
        return input_data

    def predict(self, input_data):
        return self.model.predict(input_data)

    def postprocessing(self, prediction):
        categories = ["Less Fertile", "Fertile",  "Highly Fertile"]
        index_max_predict = prediction
        return categories[index_max_predict]

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]  # only one sample
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
