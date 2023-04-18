import os

import cv2
import numpy
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.utils import CustomObjectScope


class mobile_net:
    def __init__(self):
        with CustomObjectScope({"KerasLayer": tf.keras.layers.Layer}):
            self.model = tf.keras.models.load_model(
                "agriwise/soil_type/ml_models/soil_type.h5",
                custom_objects={"KerasLayer": hub.KerasLayer},
            )

    def preprocessing(self, img_path):
        # Check if file exists
        if not os.path.exists(img_path):
            raise ValueError("Image file not found at path: " + img_path)

        # Check if file is an image with a supported format
        supported_formats = [".jpg", ".jpeg", ".png", ".bmp"]
        file_ext = os.path.splitext(img_path)[1]
        if file_ext not in supported_formats:
            raise ValueError(
                "Invalid file format. Only the following formats are supported: "
                + ", ".join(supported_formats)
            )
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError("Unable to read image file")

        # Resize image to 224x224
        img = cv2.resize(img, (224, 224))

        # Add batch dimension
        img = numpy.expand_dims(img, axis=0)

        return img

    def predict(self, input_data):
        return self.model.predict(input_data)

    def postprocessing(self, prediction):
        categories = [
            "Black Soil",
            "Cinder Soil",
            "Laterite Soil",
            "Peat Soil",
            "Yellow Soil",
        ]
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
