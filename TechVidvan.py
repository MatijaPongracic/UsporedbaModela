import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import os

gestures = {"testdata\\Call_me": "call me",
            "testdata\\Close": "fist",
            "testdata\\Live_long": "live long",
            "testdata\\OK": "okay",
            "testdata\\Peace": "peace",
            "testdata\\Rock": "rock",
            "testdata\\Smile": "smile",
            "testdata\\Stop": "stop",
            "testdata\\Thumbs_down": "thumbs down",
            "testdata\\Thumbs_up": "thumbs up"}

rezultati = {}
correct_all = 0
wrong_all = 0

# Initialize Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
with open("gesture.names", "r") as f:
    classNames = f.read().split('\n')

for key, value in gestures.items():
    # Get list of all images in the test data directory
    image_files = [f for f in os.listdir(key) if os.path.isfile(os.path.join(key, f))]
    correct = 0
    wrong = 0
    for image_file in image_files:
        # Read each image from the directory
        image_path = os.path.join(key, image_file)
        frame = cv2.imread(image_path)

        x, y, c = frame.shape

        # Flip the frame vertically
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        className = ''

        # Post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])

                # Draw landmarks on the image
                # mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                classID = np.argmax(prediction)
                className = classNames[classID]

        # cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
        #            1, (0, 0, 255), 2, cv2.LINE_AA)
        # cv2.imshow("Output", frame)
        # if cv2.waitKey(0) == ord('q'):
        #     continue

        if className == value:
            correct += 1
            correct_all += 1
        else:
            wrong += 1
            wrong_all += 1

    rezultati.update({value: (correct, wrong)})

postotak_c = round((correct_all / (correct_all + wrong_all)) * 100, 2)
postotak_w = round((wrong_all / (correct_all + wrong_all)) * 100, 2)
print(rezultati)
print(f"Correct: {correct_all} ({postotak_c}%)\nWrong: {wrong_all} ({postotak_w}%)")
cv2.destroyAllWindows()
