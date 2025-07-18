import os
import cv2
import numpy as np
from mediapipe.python.solutions.hands import Hands

DATA_DIR = "data"
OUTPUT_DIR = "processed_sequences"
SEQUENCE_LENGTH = 50

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_keypoints(results):
    # 21 landmarks per hand, 3 values (x, y, z) each
    left_hand = np.zeros(21 * 3)
    right_hand = np.zeros(21 * 3)

    # mediapipe Hands returns a list of hand_landmarks, but does not label left/right
    # We'll assign the first hand as right, second as left (mediapipe convention)
    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, handedness in enumerate(results.multi_handedness):
            label = handedness.classification[0].label
            hand_landmarks = results.multi_hand_landmarks[idx]
            keypoints = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
            if label.lower() == "left":
                left_hand = keypoints
            else:
                right_hand = keypoints
    elif results.multi_hand_landmarks:
        # If handedness info is missing, just fill right hand
        keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.multi_hand_landmarks[0].landmark]).flatten()
        right_hand = keypoints

    return np.concatenate([left_hand, right_hand])  # shape (126,)

with Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
    for label in os.listdir(DATA_DIR):
        input_folder = os.path.join(DATA_DIR, label)
        output_folder = os.path.join(OUTPUT_DIR, label)
        os.makedirs(output_folder, exist_ok=True)

        frames = []
        count = 0
        print(f"\nProcessing class: '{label}'")

        for filename in sorted(os.listdir(input_folder)):
            filepath = os.path.join(input_folder, filename)
            image = cv2.imread(filepath)
            if image is None:
                continue
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            keypoints = extract_keypoints(result)
            frames.append(keypoints)

            if len(frames) == SEQUENCE_LENGTH:
                seq_array = np.array(frames)
                if seq_array.shape == (SEQUENCE_LENGTH, 126):
                    seq_filename = os.path.join(output_folder, f"seq_{count}.npy")
                    np.save(seq_filename, seq_array)
                    print(f"Saved: {seq_filename}")
                else:
                    print(f"[SKIPPED] Sequence shape {seq_array.shape} is not (50, 126)")
                frames = []
                count += 1

        print(f"✅ Completed '{label}' - {count} sequences created.")
