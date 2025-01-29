import cv2
import numpy as np
from PIL import Image #pillow package
import os

trainer_path = "trainer"
if not os.path.exists(trainer_path):
    os.makedirs(trainer_path)  # Create the folder if it doesn't exist

path = 'samples' # Path for samples already taken

recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
# detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
detector = cv2.CascadeClassifier("D:/VISUAL_STUDIO/Project/Jarvis/Face Recognition/haarcascade_frontalface_default.xml")

if detector.empty():
    print("Error loading Haar Cascade file. Check the file path!")
    exit()

#Haar Cascade classifier is an effective object detection approach


def Images_And_Labels(path): # function to fetch the images and labels

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths: # to iterate particular image path

        gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_arr = np.array(gray_img,'uint8') #creating an array

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x,y,w,h) in faces:
            faceSamples.append(img_arr[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("Training faces. It will take a few seconds. Wait ...")

if not os.path.exists(path):
    print(f"Creating missing directory: {path}")
    os.makedirs(path)
else:
    print("Path found!")

faces,ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

recognizer.write(f"{trainer_path}/trainer.yml")  # Save trained model


print("Model trained, Now we can recognize your face.")