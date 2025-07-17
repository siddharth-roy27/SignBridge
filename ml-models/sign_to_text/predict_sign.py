import cv2
import numpy as np
import joblib

# Import the correct submodules directly from mediapipe
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks

# Load your model and actions/labels
model = joblib.load("sign_model.pkl")
# You must define your actions/labels in the same order as your model was trained
# For example:
actions = ["hello", "thankyou", "sorry", "no_sign"]  # Update as appropriate

cap = cv2.VideoCapture(0)

import pyttsx3
engine = pyttsx3.init()

last_prediction = ""
confidence_threshold = 0.8  # Adjust based on your model confidence

with Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks, HAND_CONNECTIONS)
                data = []
                for lm in hand_landmarks.landmark:
                    data.extend([lm.x, lm.y, lm.z])
                # Ensure the input shape matches what the model expects
                data_np = np.array(data).reshape(1, -1)
                # If your model supports predict_proba, use it for confidence
                if hasattr(model, "predict_proba"):
                    res = model.predict_proba(data_np)[0]
                    predicted_sign = actions[np.argmax(res)]
                    confidence = res[np.argmax(res)]
                else:
                    # Fallback: no confidence, just prediction
                    predicted_sign = model.predict(data_np)[0]
                    confidence = 1.0  # Assume full confidence if not available

                # Only say/display if new and above threshold
                if predicted_sign != last_prediction and confidence > confidence_threshold:
                    print(f"Detected: {predicted_sign} ({confidence:.2f})")
                    cv2.putText(frame, f"{predicted_sign} ({confidence:.2f})", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    engine.say(predicted_sign)
                    engine.runAndWait()
                    last_prediction = predicted_sign
                else:
                    # Still display the last prediction for user feedback
                    cv2.putText(frame, f"{last_prediction}", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Optionally reset if "no_sign" or low confidence
                if predicted_sign == "no_sign" or confidence < 0.6:
                    last_prediction = ""

        else:
            # Show last prediction or "No Hand Detected"
            cv2.putText(frame, f"{last_prediction if last_prediction else 'No Hand Detected'}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Sign Prediction", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
