import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf

SEQUENCE_LENGTH = 10
sequence = []
predictions = []
labels = ['hello', 'thankyou', 'sorry']  # update with your labels

interpreter = tf.lite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    keypoints = np.zeros(126)

    if result.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
            for i, lm in enumerate(hand_landmarks.landmark):
                if hand_idx == 0:
                    keypoints[i*3:i*3+3] = [lm.x, lm.y, lm.z]
                elif hand_idx == 1:
                    offset = 63
                    keypoints[offset + i*3:offset + i*3+3] = [lm.x, lm.y, lm.z]

    sequence.append(keypoints)
    if len(sequence) > SEQUENCE_LENGTH:
        sequence.pop(0)

    if len(sequence) == SEQUENCE_LENGTH:
        input_data = np.expand_dims(sequence, axis=0).astype(np.float32)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]['index'])
        pred = np.argmax(output)
        prob = np.max(output)

        if prob > 0.8:
            cv2.putText(frame, f'{labels[pred]} ({prob:.2f})', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Sign Detection", frame)
    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows() 