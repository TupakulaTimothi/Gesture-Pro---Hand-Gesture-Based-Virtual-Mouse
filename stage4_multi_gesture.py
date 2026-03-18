import cv2
import mediapipe as mp
import pyautogui
import math

print("Stage 4 started...")

screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not detected")
    exit()

print("Camera opened successfully")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

mp_draw = mp.solutions.drawing_utils

click_delay = 0
right_click_delay = 0

prev_y = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand in results.multi_hand_landmarks:

            lm = hand.landmark

            index = lm[8]
            thumb = lm[4]
            middle = lm[12]

            x = int(index.x * w)
            y = int(index.y * h)

            cv2.circle(frame, (x,y), 10, (0,255,0), -1)

            screen_x = screen_w * index.x
            screen_y = screen_h * index.y

            pyautogui.moveTo(screen_x, screen_y)

            # left click pinch
            dist1 = math.hypot(
                thumb.x - index.x,
                thumb.y - index.y
            )

            if dist1 < 0.03:

                if click_delay == 0:
                    pyautogui.click()
                    print("LEFT CLICK")
                    click_delay = 15

            # right click pinch
            dist2 = math.hypot(
                index.x - middle.x,
                index.y - middle.y
            )

            if dist2 < 0.03:

                if right_click_delay == 0:
                    pyautogui.rightClick()
                    print("RIGHT CLICK")
                    right_click_delay = 15

            # scroll detection
            if prev_y != 0:

                if y < prev_y - 20:
                    pyautogui.scroll(50)
                    print("SCROLL UP")

                elif y > prev_y + 20:
                    pyautogui.scroll(-50)
                    print("SCROLL DOWN")

            prev_y = y

            if click_delay > 0:
                click_delay -= 1

            if right_click_delay > 0:
                right_click_delay -= 1

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Stage 4 - Multi Gesture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()