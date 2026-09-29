from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input, decode_predictions
import numpy as np
from PIL import Image

class Predictor:

    def __init__(self):
        self.mobileNet_local = MobileNet(weights='imagenet')
        

    def preprocess(self, img_pth : str):
        img = Image.open(img_pth)
        img = img.convert("RGB")
        img = img.resize((224,224))
        npy_img = np.array(img)
        npy_img = np.expand_dims(npy_img, axis=0)

        return preprocess_input(npy_img)

    def get_predicition(self, img_pth : str):
        x = self.preprocess(img_pth)
        preds = self.mobileNet_local.predict(x)
        decoded_preds = decode_predictions(preds, top=3)[0]
        for i, (imagenet_id, label, score) in enumerate(decoded_preds):
            print(f"{i+1}. {label}: {score:.4f}")


Predictor().get_predicition("../images/Screenshot from 2025-05-06 16-35-53.png")
