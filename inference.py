import joblib
import os
import json

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "iris-model.pkl"))
    return model

def input_fn(request_body, request_content_type):
    data = json.loads(request_body)
    return data["instances"]

def predict_fn(input_data, model):
    return model.predict(input_data)

def output_fn(prediction, content_type):
    return json.dumps({"predictions": prediction.tolist()})