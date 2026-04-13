import cv2
from ultralytics import YOLO

# Загружаем модель (она сама скачается)
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Детекция
    results = model(frame)

    for r in results:
        boxes = r.boxes

        if boxes is not None:
            for box in boxes:
                cls = int(box.cls[0])

                # 0 = человек (можно отследить руки через область)
                if cls == 0:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # рамка
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

                    # центр
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    cv2.circle(frame, (cx, cy), 8, (0,0,255), -1)

                    cv2.putText(frame, "PERSON", (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("YOLO Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()