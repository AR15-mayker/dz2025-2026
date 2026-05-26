import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_result = pose.process(rgb)
    hands_result = hands.process(rgb)

    # =========================
    # 🎯 ГОЛОВА (прицел)
    # =========================
    if pose_result.pose_landmarks:
        mp_draw.draw_landmarks(
            frame,
            pose_result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # нос = центр головы
        nose = pose_result.pose_landmarks.landmark[0]
        cx, cy = int(nose.x * w), int(nose.y * h)

        # 🎯 прицел
        cv2.circle(frame, (cx, cy), 25, (0,0,255), 2)
        cv2.line(frame, (cx-40, cy), (cx+40, cy), (0,0,255), 2)
        cv2.line(frame, (cx, cy-40), (cx, cy+40), (0,0,255), 2)

        cv2.putText(frame, "HEAD LOCK", (cx - 50, cy - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    # =========================
    # ✋ РУКИ (левая / правая)
    # =========================
    if hands_result.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(hands_result.multi_hand_landmarks):

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # 👉 определение стороны
            if hands_result.multi_handedness:
                label = hands_result.multi_handedness[i].classification[0].label
                # label = "Left" или "Right"

            else:
                label = "Unknown"

            # координата запястья
            wrist = hand_landmarks.landmark[0]
            wx, wy = int(wrist.x * w), int(wrist.y * h)

            # цвет: левая = синий, правая = красный
            if label == "Left":
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)

            # текст
            cv2.putText(frame, label.upper(), (wx, wy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # точки пальцев
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id in [4, 8, 12, 16, 20]:
                    cv2.circle(frame, (cx, cy), 8, color, -1)
                else:
                    cv2.circle(frame, (cx, cy), 4, (0,255,0), -1)

    # HUD
    cv2.putText(frame, "AI TARGET SYSTEM", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("AI System PRO", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()