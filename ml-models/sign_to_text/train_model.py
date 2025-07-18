import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
import json
import joblib

DATA_PATH = 'processed_sequences'
SEQUENCE_LENGTH = 50

actions = sorted([folder for folder in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH, folder))])
print("✅ Detected classes:", actions)

X, y = [], []

for label in actions:
    label_path = os.path.join(DATA_PATH, label)
    for file in os.listdir(label_path):
        if file.endswith('.npy'):
            path = os.path.join(label_path, file)
            sequence = np.load(path)
            if sequence.shape == (SEQUENCE_LENGTH, 126):
                X.append(sequence)
                y.append(label)
            else:
                print(f"[SKIPPED] {path} has shape {sequence.shape}, expected ({SEQUENCE_LENGTH}, 126)")

X = np.array(X)
if len(X) == 0:
    print("❌ No .npy sequences found in 'processed_sequences/'. Please check your folder.")
    exit(1)
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_cat = to_categorical(y_encoded)  # One-hot encode before split

# Save LabelEncoder for inference
joblib.dump(le, "label_encoder.pkl")

# Train-test split (with one-hot encoded y)
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

# Debug prints
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("y_train example (one-hot):", y_train[0])

# Build improved LSTM model
model = Sequential()
model.add(LSTM(128, return_sequences=True, activation='relu', input_shape=(SEQUENCE_LENGTH, 126)))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(actions), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

model.fit(X_train, y_train, epochs=100, validation_data=(X_test, y_test))

# Save the model
model.save("lstm_sign_model.h5")

# Save actions (labels) for prediction
with open("actions.json", "w") as f:
    json.dump(actions, f)
