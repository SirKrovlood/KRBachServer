from EmoPy.src.fermodel import FERModel
import cv2
import numpy as np

target_emotions =  [['anger', 'fear', 'calm', 'surprise'],['happiness', 'surprise', 'disgust'],
['anger', 'fear', 'surprise'],['anger', 'fear', 'calm'],['anger', 'calm', 'happiness'],
['anger', 'fear', 'disgust'],['calm', 'surprise', 'disgust'],[ 'sadness', 'surprise', 'disgust'],
['anger', 'happiness']]

image = cv2.imread('Dummy-120.png', 0)
resized_image = cv2.resize(image, (48,48), interpolation=cv2.INTER_LINEAR)
final_image = np.array([ np.array([resized_image]).reshape([48,48, 1]) ])
print(final_image)
cv2.imwrite("oh.png", final_image)

emo_score = {'anger':0, 'fear':0, 'calm':0, 'sadness':0, 'happiness':0, 'surprise':0, 'disgust':0}
emo_coeff = {'anger':6, 'fear':4, 'calm':4, 'sadness':1, 'happiness':3, 'surprise':5, 'disgust':4}
for t in target_emotions:
	fmdl = FERModel(t, verbose=False)
	pred = fmdl.model.predict(final_image)
	normPred = [x/sum(pred[0]) for x in pred[0]]
	for i in range(len(normPred)):
		emo_score[t[i]] += round(100*normPred[i]/emo_coeff[t[i]], 2)
		print(t[i], emo_score[t[i]])
	fmdl._print_prediction(pred[0])
	print('========================================================================================')

for i in emo_score:
    print(i, emo_score[i])

print(list(emo_score.values()))
likelyIX = np.argmax(list(emo_score.values()))
print(likelyIX)
print(list(emo_score))
print(list(emo_score)[likelyIX])
