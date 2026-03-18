import cv2
import mediapipe as mp

print("Program started...")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened")
    exit()

print("Camera opened successfully")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # THIS LINE FORCES WINDOW REFRESH
    cv2.namedWindow("Stage 1 - Hand Detection", cv2.WINDOW_NORMAL)

    cv2.imshow("Stage 1 - Hand Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()