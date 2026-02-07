import cv2
import mediapipe as mp
import pyautogui
import math
import time
import numpy as np

window_name = "Mekatronik Kontrol Paneli"
cv2.namedWindow(window_name)
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)


class Finger:
    def __init__(self, point, base):
        self.x = point[0]
        self.y = point[1]
        self.dist = math.hypot(point[0] - base[0], point[1] - base[1])

# --- SETTINGS ---
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
smooth_x, smooth_y = 0, 0
yumusak_katsayi = 0.2
tap_start = 0

left_boundary, up_boundary = 200, 200
right_boundary, down_boundary = 450, 350

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    cv2.rectangle(img, (left_boundary, up_boundary ), (right_boundary, down_boundary), (255, 0, 255), 2)

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            # Wrist (Origin Point)
            wrist = (int(hand_lms.landmark[0].x * w), int(hand_lms.landmark[0].y * h))
            
            d4 = Finger((int(hand_lms.landmark[4].x * w), int(hand_lms.landmark[4].y * h)), wrist)
            d8 = Finger((int(hand_lms.landmark[8].x * w), int(hand_lms.landmark[8].y * h)), wrist)
            d12 = Finger((int(hand_lms.landmark[12].x * w), int(hand_lms.landmark[12].y * h)), wrist)
            d16 = Finger((int(hand_lms.landmark[16].x * w), int(hand_lms.landmark[16].y * h)), wrist)
            d20 = Finger((int(hand_lms.landmark[20].x * w), int(hand_lms.landmark[20].y * h)), wrist)

            # Mapping (Absolute coordinates of the index finger d8.x and d8.y)
            target_x = np.interp(d8.x, (left_boundary+20, right_boundary-20), (0, screen_w+30))
            target_y = np.interp(d8.y, (up_boundary +20, down_boundary-20), (0, screen_h+30))

            smooth_x = smooth_x + (target_x - smooth_x) * yumusak_katsayi
            smooth_y = smooth_y + (target_y - smooth_y) * yumusak_katsayi

            # DISTANCE BETWEEN FINGERS (Click and Scroll)
            dist_click = math.hypot(d8.x - d4.x, d8.y - d4.y)
            dist_scroll = math.hypot(d12.x - d8.x, d12.y - d8.y)
            

            # --- 1. BOSS KEY (PALM CONTROL) ---
            if d8.dist < 65 and d12.dist < 65 and d16.dist < 65 and d20.dist < 65:
                pyautogui.hotkey('win', 'down')
                cv2.putText(img, "BOSS KEY: DESKTOP", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                time.sleep(0.5)

            # --- 1. HYPBRID (X: Voice, Y: Scroll) ---
            if dist_scroll < 30:
                # CENTER POINTS (BASED ON OUR RECTANGLE)
                center_x = left_boundary + (right_boundary - left_boundary) / 2
                merkez_y = up_boundary  + (down_boundary- up_boundary ) / 2

                # A) VOICE CHECK    
                # If you move your hand to the right, it's SOUND++, if you move it to the left, it's SOUND--
                if d8.x > center_x + 50:
                    pyautogui.press("volumeup")
                    cv2.putText(img, "SES ++", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                elif d8.x < center_x - 50:
                    pyautogui.press("volumedown")
                    cv2.putText(img, "SES --", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                # B) SCROLL CONTROL 
            
                elif d8.y < merkez_y - 40:
                    pyautogui.scroll(20)
                    cv2.putText(img, "SCROLL UP", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                elif d8.y > merkez_y + 40:
                    pyautogui.scroll(-20)
                    cv2.putText(img, "SCROLL DOWN", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)





            # --- 3.MOVE AND CLICK ---
            elif dist_click < 30:
                if tap_start == 0:
                     tap_start = time.time()
                time_past = time.time() - tap_start
                if time_past  > 0.15:
                    pyautogui.moveTo(int(smooth_x), int(smooth_y))
                    cv2.putText(img, "MOUSE DRAG", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            else:
                if tap_start != 0:
                    time_past  = time.time() - tap_start
                    if time_past  < 0.4:
                        pyautogui.click()
                        cv2.putText(img, "CLICK!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    tap_start = 0

            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("ISTUN MECHATRONIC - Master Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
