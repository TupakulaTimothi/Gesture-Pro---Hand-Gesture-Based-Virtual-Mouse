import cv2
import mediapipe as mp
import pyautogui
import math

print("Stage 3 started...")

# Screen size
screen_width, screen_height = pyautogui.size()

# Camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()

print("Camera opened successfully")

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

mp_draw = mp.solutions.drawing_utils

click_delay = 0

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

            lm = hand_landmarks.landmark

            # index finger tip
            index = lm[8]

            # thumb tip
            thumb = lm[4]

            x = int(index.x * frame_width)
            y = int(index.y * frame_height)

            cv2.circle(frame, (x,y), 10, (0,255,0), -1)

            # move cursor
            screen_x = screen_width * index.x
            screen_y = screen_height * index.y

            pyautogui.moveTo(screen_x, screen_y)

            # distance between thumb and index
            dist = math.hypot(
                thumb.x - index.x,
                thumb.y - index.y
            )

            # pinch detection
            if dist < 0.03:

                if click_delay == 0:
                    pyautogui.click()
                    print("CLICK")
                    click_delay = 15

            if click_delay > 0:
                click_delay -= 1

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Stage 3 - Click Gesture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()