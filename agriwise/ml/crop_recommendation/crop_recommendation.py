import numpy
import joblib
import pandas as pd

class RandomForestClassifier:
    def __init__(self):
        self.model = joblib.load('./random_forest.joblib')

    def preprocessing(self, input_data):
        # JSON to pandas DataFrame
        input_data = pd.DataFrame(input_data, index=[0])

        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)
        
    def postprocessing(self, prediction):
        categories = ['apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee',
                      'cotton', 'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans', 'mungbean', 'muskmelon', 'orange', 'papaya', 'pigeonpeas', 'pomegranate', 'rice', 'watermelon']
        index_max_predict = numpy.argmax(prediction)
        return categories[index_max_predict]
        

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]  # only one sample
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

      
        return prediction