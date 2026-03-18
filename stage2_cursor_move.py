import cv2
import mediapipe as mp
import pyautogui

print("Stage 2 started...")

# Screen size
screen_width, screen_height = pyautogui.size()

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()

print("Camera opened successfully")

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

mp_draw = mp.solutions.drawing_utils

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # index finger tip
            index_finger = hand_landmarks.landmark[8]

            x = int(index_finger.x * frame_width)
            y = int(index_finger.y * frame_height)

            # draw circle on finger
            cv2.circle(frame, (x, y), 10, (0,255,0), -1)

            # convert to screen coordinates
            screen_x = screen_width * index_finger.x
            screen_y = screen_height * index_finger.y

            # move mouse
            pyautogui.moveTo(screen_x, screen_y)

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Stage 2 - Cursor Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()