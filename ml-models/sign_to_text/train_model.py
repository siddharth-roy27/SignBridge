import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

DATA_PATH = 'data'
SEQUENCE_LENGTH = 10

# Load sequences and labels
X, y = [], []

for label in os.listdir(DATA_PATH):
    label_path = os.path.join(DATA_PATH, label)
    if not os.path.isdir(label_path):
        continue
    for file in os.listdir(label_path):
        if file.endswith('.npy'):
            sequence = np.load(os.path.join(label_path, file))
            if sequence.shape[0] == SEQUENCE_LENGTH:
                X.append(sequence)
                y.append(label)

X = np.array(X)
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_cat = to_categorical(y_encoded)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

# Build LSTM model
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(SEQUENCE_LENGTH, X.shape[2])))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(np.unique(y_encoded)), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

model.fit(X_train, y_train, epochs=30, validation_data=(X_test, y_test))

# Save the model
model.save("lstm_sign_model.h5")
