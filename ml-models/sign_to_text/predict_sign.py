import cv2
import numpy as np
from collections import deque
from utils import extract_hand_keypoints
import os
import json
import time

# Import the correct submodules directly from mediapipe
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks

# Choose which model to load: scikit-learn (joblib) or deep learning (Keras)
USE_DEEP_LEARNING_MODEL = True  # Set to False to use joblib model

if USE_DEEP_LEARNING_MODEL:
    from tensorflow.keras.models import load_model
    model = load_model("lstm_sign_model.h5")

else:
    import joblib
    model = joblib.load("sign_model.pkl")

# Load actions (class labels) from actions.json
with open("actions.json", "r") as f:
    actions = json.load(f)

import pyttsx3
engine = pyttsx3.init()

last_prediction = ""
last_confidence = 0.0
spoken_recently = False
confidence_threshold = 0.8  # Adjust based on your model confidence
last_prediction_time = 0
prediction_display_duration = 2  # seconds

SEQUENCE_LENGTH = 50  # Make sure this matches your training
sequence = deque(maxlen=SEQUENCE_LENGTH)

cap = cv2.VideoCapture(0)

def extract_both_hands_keypoints(multi_hand_landmarks):
    keypoints = []
    if multi_hand_landmarks:
        for hand_landmarks in multi_hand_landmarks[:2]:
            if hand_landmarks and len(hand_landmarks.landmark) == 21:
                pts = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                keypoints.append(pts.flatten())
    while len(keypoints) < 2:
        keypoints.append(np.zeros(63))  # Pad if only one hand
    return np.concatenate(keypoints)  # Shape: (126,)

with Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Debug: print Mediapipe hand detection result
        print("Hand landmarks:", results.multi_hand_landmarks)

        # Draw landmarks for visualization
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks, HAND_CONNECTIONS)

        # Skip prediction if no hand detected
        if results.multi_hand_landmarks:
            keypoints = extract_both_hands_keypoints(results.multi_hand_landmarks)
            sequence.append(keypoints)

            if len(sequence) == SEQUENCE_LENGTH:
                input_data = np.expand_dims(sequence, axis=0)
                print("Input shape to model:", input_data.shape)
                if input_data.shape != (1, SEQUENCE_LENGTH, 126):
                    print("⚠️ Wrong input shape:", input_data.shape)
                    continue  # Skip this frame

                if USE_DEEP_LEARNING_MODEL:
                    res = model.predict(input_data)[0]
                    predicted_sign = actions[np.argmax(res)]
                    confidence = res[np.argmax(res)]
                else:
                    if hasattr(model, "predict_proba"):
                        res = model.predict_proba(input_data.reshape(1, -1))[0]
                        predicted_sign = actions[np.argmax(res)]
                        confidence = res[np.argmax(res)]
                    else:
                        predicted_sign = model.predict(input_data.reshape(1, -1))[0]
                        confidence = 1.0

                if confidence > confidence_threshold:
                    if predicted_sign != last_prediction:
                        print(f"New Prediction: {predicted_sign} ({confidence:.2f})")
                        engine.say(predicted_sign)
                        engine.runAndWait()
                        last_prediction = predicted_sign
                        last_confidence = confidence
                        last_prediction_time = time.time()
                        spoken_recently = True
                    else:
                        # Same as before, but confident
                        last_confidence = confidence
                        last_prediction_time = time.time()
                else:
                    last_prediction = ""
                    last_confidence = 0.0
                    spoken_recently = False
        else:
            # No hands detected
            sequence.clear()
            last_prediction = ""
            last_confidence = 0.0
            spoken_recently = False

        # Display current prediction on screen with timer
        current_time = time.time()
        if current_time - last_prediction_time < prediction_display_duration and last_prediction:
            label = f"{last_prediction} ({last_confidence:.2f})"
            color = (0, 255, 0)
        else:
            label = "No hand detected"
            color = (0, 0, 255)
        
        cv2.putText(frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Sign Prediction", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
