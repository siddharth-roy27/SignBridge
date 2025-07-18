import cv2
import os
import numpy as np
import time
import mediapipe as mp

# --- CONFIG ---
SIGN_RECORD_SECONDS = 5
TARGET_FPS = 10
FRAMES_REQUIRED = SIGN_RECORD_SECONDS * TARGET_FPS
MAX_MISSED_FRAMES = int(FRAMES_REQUIRED * 0.2)  # tolerate 20% missed frames
HAND_SMOOTH_START = 5  # number of consistent frames before auto start

# --- PATH SETUP ---
DATA_PATH = "data"
sign_name = input("Enter the name of the sign to record: ").strip().lower()
sign_dir = os.path.join(DATA_PATH, sign_name)
os.makedirs(sign_dir, exist_ok=True)
existing = [int(f.split('_')[-1].split('.')[0]) for f in os.listdir(sign_dir) if f.startswith("seq_")]
sequence_num = max(existing, default=0) + 1

# --- MEDIAPIPE SETUP ---
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks

hands = Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def extract_landmarks(multi_hand_landmarks):
    """Extract 2-hand landmarks (pad if 1 or 0)."""
    keypoints = []
    if multi_hand_landmarks:
        for hand in multi_hand_landmarks[:2]:
            pts = np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark])
            keypoints.append(pts.flatten())
    while len(keypoints) < 2:
        keypoints.append(np.zeros(63))  # 21 landmarks x 3 coords
    return np.concatenate(keypoints)

# --- CAMERA ---
cap = cv2.VideoCapture(0)
print(f"[INFO] Recording sign '{sign_name}' in {sign_dir}/seq_<n>.npy")

buffer = []
smooth_counter = 0

def record_sequence(cap, hands, sign_dir, sequence_num):
    sequence = []
    missed = 0
    while len(sequence) < FRAMES_REQUIRED:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            keypoints = extract_landmarks(results.multi_hand_landmarks)
            sequence.append(keypoints)
            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks, HAND_CONNECTIONS)
        else:
            missed += 1
            sequence.append(np.zeros(126))  # empty frame placeholder

        remaining = FRAMES_REQUIRED - len(sequence)
        cv2.putText(frame, f"Recording... {remaining} frames left",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Sign Recorder", frame)
        if cv2.waitKey(int(1000 / TARGET_FPS)) & 0xFF == ord('q'):
            raise KeyboardInterrupt

    # Save only if enough valid frames
    if missed <= MAX_MISSED_FRAMES:
        np.save(os.path.join(sign_dir, f"seq_{sequence_num}.npy"), np.array(sequence))
        print(f"[SAVED] Sequence #{sequence_num} with {missed} dropped frames.")
        return True
    else:
        print(f"[SKIPPED] Too many missed frames: {missed}/{FRAMES_REQUIRED}")
        return False

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Start condition — hand detected for multiple consecutive frames
        if results.multi_hand_landmarks:
            smooth_counter += 1
        else:
            smooth_counter = 0

        cv2.putText(frame, f"Waiting for hands... [{smooth_counter}/{HAND_SMOOTH_START}]",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame, "Press 'm' to record manually", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 255), 2)

        # Start recording automatically
        if smooth_counter >= HAND_SMOOTH_START:
            print(f"[INFO] Starting auto recording for {SIGN_RECORD_SECONDS}s...")
            success = record_sequence(cap, hands, sign_dir, sequence_num)
            if success:
                sequence_num += 1
            smooth_counter = 0  # reset for next recording

        # Show preview
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks, HAND_CONNECTIONS)
        cv2.imshow("Sign Recorder", frame)

        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m'):
            print(f"[INFO] Manual recording started for {SIGN_RECORD_SECONDS}s...")
            success = record_sequence(cap, hands, sign_dir, sequence_num)
            if success:
                sequence_num += 1
            smooth_counter = 0  # reset for next recording

except KeyboardInterrupt:
    print("[STOPPED] Manually interrupted.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
