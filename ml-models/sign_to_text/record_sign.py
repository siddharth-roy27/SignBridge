import cv2
import os
import mediapipe as mp
import numpy as np
import time

DATA_PATH = 'data'
NUM_FRAMES = 10
SIGN_LABEL = input("Enter the sign label (e.g., hello, thanks): ").strip()

if not SIGN_LABEL:
    print("Label cannot be empty.")
    exit(1)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Could not open webcam. Try changing the index to 1 or 2.")
    exit(1)

print("Starting recording in 3 seconds...")
time.sleep(3)

sample_id = 0
os.makedirs(f"{DATA_PATH}/{SIGN_LABEL}", exist_ok=True)

while True:
    keypoints_sequence = []
    print(f"Recording sample {sample_id}...")

    for _ in range(NUM_FRAMES):
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame from webcam.")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        keypoints = np.zeros(126)  # 2 hands * 21 landmarks * 3 (x,y,z)

        if result.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                for i, lm in enumerate(hand_landmarks.landmark):
                    if hand_idx == 0:
                        keypoints[i*3:i*3+3] = [lm.x, lm.y, lm.z]
                    elif hand_idx == 1:
                        offset = 63
                        keypoints[offset + i*3:offset + i*3+3] = [lm.x, lm.y, lm.z]
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        keypoints_sequence.append(keypoints)
        cv2.putText(frame, f"Recording: {SIGN_LABEL} | Frame: {len(keypoints_sequence)}/{NUM_FRAMES}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Recording", frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Save sequence if correct number of frames
    if len(keypoints_sequence) == NUM_FRAMES:
        np.save(f"{DATA_PATH}/{SIGN_LABEL}/{SIGN_LABEL}_{sample_id}.npy", np.array(keypoints_sequence))
        print(f"Saved {SIGN_LABEL}_{sample_id}.npy")
        sample_id += 1
    else:
        print("Sample discarded (not enough frames).")

    # Press Esc to quit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
