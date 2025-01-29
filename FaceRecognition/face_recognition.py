import cv2
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')  # Load the trained model
face_cascade = cv2.CascadeClassifier("D:/VISUAL_STUDIO/Project/Jarvis/Face Recognition/haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)  # Open webcam

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id, conf = recognizer.predict(roi_gray)

        if conf < 100:  # Confidence threshold (lower is better)
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = f"User {id}"
            cv2.putText(frame, name, (x, y - 10), font, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        else:
            cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
