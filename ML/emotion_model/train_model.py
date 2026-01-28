import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

# 1. Load the preprocessed data
# These should be in the same folder if you ran preprocess.py there
X = np.load('X_features.npy')
y = np.load('y_labels.npy')

# Reshape for the 1D CNN: (samples, time_steps, features)
# Your features are likely (40 MFCCs x 160 time steps) or vice-versa
# If you used the previous extract_features, it's (40, 160). We need it to be (160, 40)
X = np.array([f.T if f.shape[0] == 40 else f for f in X])

# 2. Split into Training (80%) and Testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Build the CNN-GRU Architecture (Module 3 in your PDF)
model = models.Sequential([
    # CNN Block: Extracts spatial features (energy, pitch patterns)
    layers.Conv1D(64, 3, activation='relu', input_shape=(X.shape[1], X.shape[2])),
    layers.BatchNormalization(),
    layers.MaxPooling1D(2),
    layers.Dropout(0.2),

    # GRU Block: Extracts temporal features (speed, rhythm, pauses)
    layers.GRU(128, return_sequences=False),
    
    # Emotion Embedding Layer (The vector for Module 4!)
    layers.Dense(128, activation='relu', name="emotion_embedding"),
    
    # Final Classification Layer
    layers.Dense(7, activation='softmax') # 7 emotions in EMO-DB
])

# 4. Compile and Train
model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

print("Starting training on EMO-DB...")
history = model.fit(X_train, y_train, 
                    epochs=50, 
                    batch_size=32, 
                    validation_data=(X_test, y_test))

# 5. Save the Full Model (Architecture + Weights)
# This prevents having to retrain after you shut down your laptop
model.save('emotion_encoder_v1.h5')
print("\nSuccess! Model saved as 'emotion_encoder_v1.h5'")