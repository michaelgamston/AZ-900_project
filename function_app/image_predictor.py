from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input, decode_predictions
import numpy as np
from PIL import Image
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import datetime
import uuid

class Predictor:

    def __init__(self):
        self.mobileNet_local = MobileNet(weights='imagenet')
        
    def __preprocess(self, img_pth):
        img = Image.open(img_pth)
        img = img.convert("RGB")
        img = img.resize((224,224))
        npy_img = np.array(img)
        npy_img = np.expand_dims(npy_img, axis=0)

        return preprocess_input(npy_img)

    def get_prediction(self, img_pth):
        x = self.__preprocess(img_pth)
        preds = self.mobileNet_local.predict(x)
        decoded_preds = decode_predictions(preds, top=1)[0][0]
        print(decoded_preds)
        #return label and confidence score
        return decoded_preds[1], decoded_preds[2]

    
        # for i, (imagenet_id, label, score) in enumerate(decoded_preds):
        #     print(f"{i+1}. {label}: {score:.4f}")


#Predictor().get_prediction("../images/Screenshot from 2025-05-06 16-35-53.png")

class CosmosDB_handler:

    def __init__(self):
        account_url = "https://az900results.documents.azure.com:443/"
        credential = DefaultAzureCredential()
        self.client = CosmosClient(account_url, credential=credential)

    def post_result(self, label, confidence):

        database = self.client.get_database_client("image-results")
        container = database.get_container_client("predictions")

        document = {
            "id": str(uuid.uuid4()),
            "prediction_label": label,
            "filename": "test.jpg",
            "confidence": float(confidence),
            "timestamp": str(datetime.datetime.now())
        }

        container.create_item(body=document)

#temp handler function
def handle_event(img_pth):

    predictor = Predictor()
    cosmos_handler = CosmosDB_handler()

    label, confidence = predictor.get_prediction(img_pth)
    cosmos_handler.post_result(label, confidence)

handle_event("../images/Screenshot from 2025-05-06 16-35-53.png")