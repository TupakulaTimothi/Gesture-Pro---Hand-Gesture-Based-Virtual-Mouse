import cv2
import mediapipe as mp
import pyautogui
import math

# ==============================
# GLOBAL VARIABLES
# ==============================

gesture_running = False
current_action = "None"

cap = None

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

mp_draw = mp.solutions.drawing_utils

click_delay = 0
right_click_delay = 0
prev_y = 0

# ==============================
# GESTURE MAPPING
# ==============================

gesture_mapping = {
    "PINCH_THUMB_INDEX": "LEFT CLICK",
    "PINCH_INDEX_MIDDLE": "RIGHT CLICK",
    "MOVE_UP": "SCROLL UP",
    "MOVE_DOWN": "SCROLL DOWN",
    "CURSOR_MOVE": "CURSOR MOVE"
}

gesture_description = {
    "PINCH_THUMB_INDEX": "Pinch Thumb + Index",
    "PINCH_INDEX_MIDDLE": "Pinch Index + Middle",
    "MOVE_UP": "Move Hand Up",
    "MOVE_DOWN": "Move Hand Down",
    "CURSOR_MOVE": "Move Index Finger"
}

# ==============================
# START / STOP SYSTEM
# ==============================

def start_gesture():
    global gesture_running, cap

    if not gesture_running:
        cap = cv2.VideoCapture(0)
        gesture_running = True


def stop_gesture():
    global gesture_running, cap

    gesture_running = False

    if cap:
        cap.release()

# ==============================
# UPDATE GESTURE MAPPING
# ==============================

def update_mapping(gesture, action):

    # remove same action from other gestures
    for g in gesture_mapping:
        if gesture_mapping[g] == action:
            gesture_mapping[g] = "NONE"

    # assign new action
    gesture_mapping[gesture] = action


# ==============================
# GET MAPPING FOR UI
# ==============================

def get_mapping_with_description():

    data = {}

    for g in gesture_mapping:
        data[g] = {
            "description": gesture_description[g],
            "action": gesture_mapping[g]
        }

    return data


# ==============================
# ASSISTANT REPLIES
# ==============================

def gesture_assistant_reply(msg):

    msg = msg.lower()

    if "gesture" in msg:
        return "Use your hand gestures to control the mouse."

    if "click" in msg:
        return "Pinch thumb and index finger to click."

    if "scroll" in msg:
        return "Move your hand up or down."

    return "Gesture assistant ready."

# ==============================
# CAMERA STREAM
# ==============================

def generate_frames():

    global current_action
    global click_delay
    global right_click_delay
    global prev_y

    while gesture_running:

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

                cv2.circle(frame,(x,y),10,(0,255,0),-1)

                # move cursor
                screen_x = screen_w * index.x
                screen_y = screen_h * index.y

                pyautogui.moveTo(screen_x,screen_y)

                current_action = "CURSOR MOVE"

                # LEFT CLICK
                dist1 = math.hypot(
                    thumb.x - index.x,
                    thumb.y - index.y
                )

                if dist1 < 0.03 and click_delay == 0:

                    if gesture_mapping["PINCH_THUMB_INDEX"] == "LEFT CLICK":
                        pyautogui.click()
                        current_action = "LEFT CLICK"

                    click_delay = 15

                # RIGHT CLICK
                dist2 = math.hypot(
                    index.x - middle.x,
                    index.y - middle.y
                )

                if dist2 < 0.03 and right_click_delay == 0:

                    if gesture_mapping["PINCH_INDEX_MIDDLE"] == "RIGHT CLICK":
                        pyautogui.rightClick()
                        current_action = "RIGHT CLICK"

                    right_click_delay = 15

                # SCROLL
                if prev_y != 0:

                    if y < prev_y - 20:

                        if gesture_mapping["MOVE_UP"] == "SCROLL UP":
                            pyautogui.scroll(50)
                            current_action = "SCROLL UP"

                    elif y > prev_y + 20:

                        if gesture_mapping["MOVE_DOWN"] == "SCROLL DOWN":
                            pyautogui.scroll(-50)
                            current_action = "SCROLL DOWN"

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

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame + b'\r\n')