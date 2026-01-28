import os
import librosa
import numpy as np

# Map the German letters to numbers for the model
label_map = {'W':0, 'L':1, 'E':2, 'A':3, 'F':4, 'T':5, 'N':6}
#data_path = # "../../" means go up two folders (out of Emotion_Model, then out of ML)
data_path = "../../Data/archive/wav/" # Path to your extracted folder

def extract_features(file_path):
    # Load audio at 16kHz (Standard for EMO-DB)
    audio, sr = librosa.load(file_path, sr=16000)
    # Extract MFCCs (captures the "texture" of the emotion)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    # Ensure all clips are the same length (pad with zeros if too short)
    if mfccs.shape[1] < 160:
        mfccs = np.pad(mfccs, ((0,0), (0, 160 - mfccs.shape[1])))
    return mfccs[:, :160]

features = []
labels = []

for filename in os.listdir(data_path):
    if filename.endswith(".wav"):
        # The 6th character is the label
        emotion_letter = filename[5].upper()
        if emotion_letter in label_map:
            path = os.path.join(data_path, filename)
            features.append(extract_features(path))
            labels.append(label_map[emotion_letter])

# Save these so you don't have to extract them again
np.save('X_features.npy', np.array(features))
np.save('y_labels.npy', np.array(labels))
print("Preprocessing complete!")