def extract_hand_keypoints(multi_hand_landmarks):
    keypoints = [0.0] * 126
    if multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(multi_hand_landmarks):
            for i, lm in enumerate(hand_landmarks.landmark):
                if hand_idx == 0:
                    keypoints[i*3:i*3+3] = [lm.x, lm.y, lm.z]
                elif hand_idx == 1:
                    offset = 63
                    keypoints[offset + i*3:offset + i*3+3] = [lm.x, lm.y, lm.z]
    return keypoints
