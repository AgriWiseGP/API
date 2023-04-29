import os

import numpy
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import CustomObjectScope


class mobile_net:
    def __init__(self):
        with CustomObjectScope({"KerasLayer": tf.keras.layers.Layer}):
            self.model = tf.keras.models.load_model(
                "agriwise/plant_diseases/ml_model/class2.h5",
                custom_objects={"KerasLayer": hub.KerasLayer},
            )

    def preprocessing(self, img_path):
        file_img_path = img_path.lstrip("/")
        if not os.path.exists(file_img_path):
            raise ValueError("Image file not found at path: " + file_img_path)
        # Check if file is an image with a supported format
        supported_formats = [".jpg", ".jpeg", ".png", ".bmp", ".JPG"]
        file_ext = os.path.splitext(file_img_path)[1]
        if file_ext not in supported_formats:
            raise ValueError(
                "Invalid file format. Only the following formats are supported: "
                + ", ".join(supported_formats)
            )
        # Load image

        img = image.load_img(file_img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = numpy.expand_dims(img_array, axis=0)

        return img_array

    def predict(self, input_data):
        return self.model.predict(input_data)

    def postprocessing(self, prediction):
        categories = [
            "Apple___Apple_scab",
            "Apple___Black_rot",
            "Apple___Cedar_apple_rust",
            "Apple___healthy",
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
            "Corn_(maize)___Common_rust_",
            "Corn_(maize)___Northern_Leaf_Blight",
            "Corn_(maize)___healthy",
            "Grape___Black_rot",
            "Grape___Esca_(Black_Measles)",
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            "Grape___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato___Bacterial_spot",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___Leaf_Mold",
            "Tomato___Septoria_leaf_spot",
            "Tomato___Spider_mites Two-spotted_spider_mite",
            "Tomato___Target_Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "Tomato___Tomato_mosaic_virus",
            "Tomato___healthy",
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
