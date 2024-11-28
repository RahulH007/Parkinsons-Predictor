import pickle
import numpy as np
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, '/Users/bramhabajannavar/Desktop/Parkinsons/Parkinsons/main/models/parkinsons_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, '/Users/bramhabajannavar/Desktop/Parkinsons/Parkinsons/main/models/scaler.pkl')


with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

with open(SCALER_PATH, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)


def predict(input_features):
    """
    Predict the likelihood of Parkinson's disease based on input features.

    Args:
        input_features (list): List of 22 numeric input features.

    Returns:
        float: The predicted probability of Parkinson's disease.
    """
  
    input_features = np.array(input_features).reshape(1, -1)

    
    scaled_features = scaler.transform(input_features)

    prediction_prob = model.predict_proba(scaled_features)
    return prediction_prob[0][1]
