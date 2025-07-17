import cv2
import mediapipe as mp

# Initialize MediaPipe hands and drawing utils
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def detect_hands_from_frame(frame, max_num_hands=2):
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=max_num_hands,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    ) as hands:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        landmarks_list = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_coords = []
                for lm in hand_landmarks.landmark:
                    hand_coords.append([lm.x, lm.y, lm.z])
                landmarks_list.append(hand_coords)
                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
        return frame, landmarks_list

def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame_with_landmarks, landmarks_list = detect_hands_from_frame(frame, max_num_hands=2)
        if landmarks_list:
            print("Frame keypoints:", landmarks_list)
        cv2.imshow('MediaPipe Hands', frame_with_landmarks)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit.
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
