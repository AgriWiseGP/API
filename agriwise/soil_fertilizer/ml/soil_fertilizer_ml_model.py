import joblib
import numpy
import pandas as pd


class SoilFertilizerMLModel:
    def __init__(self):
        self.model = joblib.load(
            "agriwise/soil_fertilizer/ml/random_forest_fertilizer.joblib"
        )
        self.soli_type = [
            "Clayey",
            "alluvial",
            "clay loam",
            "coastal",
            "laterite",
            "sandy",
            "silty clay",
        ]

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        if input_data["Crop"][0] == "rice":
            input_data["Crop"] = 1
        else:
            input_data["Crop"] = 0
        input_data["Soil"] = self.soli_type.index(input_data["Soil"][0])
        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, prediction):
        categories = [
            "DAP",
            "DAP and MOP",
            "Good NPK",
            "MOP",
            "Urea",
            "Urea and DAP",
            "Urea and MOP",
        ]
        index_max_predict = numpy.argmax(prediction)
        return categories[index_max_predict]

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        return prediction
