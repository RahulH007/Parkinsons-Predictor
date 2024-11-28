#!/usr/bin/env python
# coding: utf-8

# In[102]:


import os
import pickle
import pyaudio
import wave

# Define the complete path to the .pkl files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'main/models/parkinsons_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'main/models/scaler.pkl')
IMPUTER_PATH = os.path.join(BASE_DIR, 'main/models/imputer.pkl')

# Load the model and scaler from pickle files
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

with open(SCALER_PATH, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Load the saved imputer (to handle missing values in the features)
with open(IMPUTER_PATH, 'rb') as imputer_file:
    imputer = pickle.load(imputer_file)


# In[103]:


def record_audio(filename='user_audio.wav', duration=25, sample_rate=16000):
    """Record audio from the microphone and save it as a .wav file."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
    
    print("Recording...")
    print("Please Read the Following Paragrapgh...")
    print('''The quick brown fox jumps over the lazy dog near a quiet riverbank.
     As the sun sets, the calm breeze rustles the leaves, creating a soothing sound.
     In the distance, a clock tower chimes, marking the end of another day. Every moment counts,
     and every word we speak carries a meaning, shaping the world around us. 
     Speak clearly, and let your voice express the thoughts within your mind.''')
    frames = []
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))


# In[104]:


import librosa
import numpy as np

def extract_features(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Extract MFCC (13 coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_scaled = np.mean(mfcc.T, axis=0)

    # Extract additional features
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85))
    chroma_mean = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))

    # Combine features
    features = np.hstack((mfcc_scaled, zcr, rolloff, chroma_mean))  # Shape: (16,)

    # Pad to 22 features if needed
    if len(features) < 22:
        features = np.pad(features, (0, 22 - len(features)), 'constant')

    return features


# In[ ]:


# print(f"Scaler expected input shape: {scaler.n_features_in_}")


# In[ ]:





# In[ ]:


def predict_parkinsons(audio_file):
    """Predict Parkinson's disease from an audio file."""
    print("Starting feature extraction...")
    features = extract_features(audio_file)
    print(f"Extracted features: {features}")

    # Check feature length
    if len(features) != scaler.n_features_in_:
        raise ValueError(f"Feature shape mismatch: expected {scaler.n_features_in_} features, got {len(features)}")
    
    print("Scaling features...")
    features_scaled = scaler.transform([features])
    print(f"Scaled features: {features_scaled}")

    print("Making prediction...")
    prediction = model.predict(features_scaled)
    prediction_proba = model.predict_proba(features_scaled)
    print(f"Prediction probabilities: {prediction_proba[0]}")

    # Return final result
    if prediction_proba[0][0] > 0.8:
        return f"Parkinson's disease detected."
    else:
        return f"No Parkinson's disease detected !!!!!"


# In[107]:


try:
    predict_parkinsons('user_audio.wav')
except Exception as e:
    print(f"Error: {e}")


# In[ ]:





# In[ ]:




