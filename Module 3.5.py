import cv2, time, pyautogui, mediapipe as mp, numpy as np
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

scroll_speed = 300
scroll_delay = 1
cam_width, cam_height = 640, 480
def detect_gesture(hand_landmarks,handedness):
    fingers = []
    tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
             mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    if handedness == "Right":
        if thumb_tip.x < thumb_ip.x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if thumb_tip.x > thumb_ip.x:
            fingers.append(1)
        else:
            fingers.append(0)
    return "Scroll_Up" if sum(fingers) == 5 else "Scroll_Down" if sum(fingers) == 0 else None
cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    img= cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1)
    results = hands.process(img)
    gesture,handedness = None,unknown
    if results.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            handedness = hand_handedness.classification[0].label
            gesture = detect_gesture(hand_landmarks)
            if (time.time() - last_scroll_time) > scroll_delay:
                if gesture == "Scroll_Up":
                    pyautogui.scroll(scroll_speed)
                    last_scroll_time = time.time()
                elif gesture == "Scroll_Down":
                    pyautogui.scroll(-scroll_speed)
                    last_scroll_time = time.time()
    fps = 1 / (time.time() - last_frame_time) if last_frame_time else 0
    last_frame_time = time.time()
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Based Scrolling", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()   
cv2.destroyAllWindows()
