import json
# import cv2 as cv
from PIL import Image
import numpy as np
import scipy.io
from keras.models import load_model


# pomocna funkcija za pretvaranje slike iz bgr u rgb
# radi ako je dan i alhpa property
def convert_to_rgb(image):
    sub = image.convert("RGBA")
    data = np.array(sub)
    red, green, blue = data.T
    data = np.array([blue, green, red])
    data = data.transpose()
    sub = Image.fromarray(data)
    return sub


model = load_model("cnn_model.h5")
width, height = 128, 128

# s obzirom da koristimo AWS EC2 (amazon-linux) za server
# namamo podrsku za gui pa cv library ne radi nativno
# bgr_img = cv.imread("data/for_validation/image.jpg")
bgr_image = Image.open("data/for_validation/image.jpg")
# bgr_img = cv.resize(bgr_img, (width, height), cv.INTER_CUBIC)
bgr_image = bgr_image.resize((width, height))
# rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
# pretvaramo sliku u rgb
rgb_img = Image.fromarray(np.array(bgr_image)[:, :, ::-1])
rgb_img = np.expand_dims(rgb_img, 0)
preds = model.predict(rgb_img)
prob = np.max(preds)
class_id = np.argmax(preds)

cars_meta = scipy.io.loadmat('cars_meta')
class_names = cars_meta['class_names']
class_names = np.transpose(class_names)

results = []
text = ('Predict: {}, prob: {}'.format(class_names[class_id][0][0], prob))
results.append({'label': class_names[class_id][0][0], 'prob': '{:.4}'.format(prob)})

print(results)
# spremamo rezultate da ih app.py (ili neka druga skripta) moze procitat
with open('results.json', 'w') as file:
    json.dump(results, file, indent=4)
