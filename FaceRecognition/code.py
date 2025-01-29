import cv2
import os

face_cascade = cv2.CascadeClassifier("D:/VISUAL_STUDIO/Project/Jarvis/Face Recognition/haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)  # Open webcam

user_id = input("Enter user ID (numeric): ")  # Unique ID for the person
count = 0
save_path = "samples"

if not os.path.exists(save_path):
    os.makedirs(save_path)

while count < 20:  # Capture 20 images per person
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face_img = gray[y:y+h, x:x+w]
        filename = f"{save_path}/User.{user_id}.{count}.jpg"
        cv2.imwrite(filename, face_img)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Face Capture', frame)
    if cv2.waitKey(100) & 0xFF == 27:  # Press ESC to exit early
        break

cap.release()
cv2.destroyAllWindows()
print("Face dataset collection completed!")
