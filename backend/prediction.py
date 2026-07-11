import os
import pickle
import numpy as np

# get project root directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# build correct model path
model_path = os.path.join(base_dir, "model", "model.pk1")

# load model
model = pickle.load(open(model_path, "rb"))

def predict_quality(data):
    prediction = model.predict(np.array(data).reshape(1, -1))
    return prediction[0]