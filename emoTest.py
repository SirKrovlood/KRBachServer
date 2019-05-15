from EmoPy.src.fermodel import FERModel
import cv2

target_emotions =  [ 'sadness', 'surprise', 'disgust']
model = FERModel(target_emotions, verbose=True)

model.predict("Dummy-11.png")
