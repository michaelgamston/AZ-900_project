from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input, decode_predictions
import numpy as np
from PIL import Image
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
import datetime
import uuid
import os 
import io

class Predictor:

    def __init__(self):
        self.mobileNet_local = MobileNet(weights='imagenet')
        
    def __preprocess(self, raw_img):
        img = Image.open(io.BytesIO(raw_img))
        img = img.convert("RGB")
        img = img.resize((224,224))
        npy_img = np.array(img)
        npy_img = np.expand_dims(npy_img, axis=0)

        return preprocess_input(npy_img)

    def get_prediction(self, raw_img):
        x = self.__preprocess(raw_img)
        preds = self.mobileNet_local.predict(x, verbose=0)
        decoded_preds = decode_predictions(preds, top=1)[0][0]
        
        return decoded_preds[1], decoded_preds[2]


class CosmosDB_handler:

    def __init__(self):

        account_url = os.environ["COSMOS_URL"]
        credential = DefaultAzureCredential()
        client = CosmosClient(account_url, credential=credential)
        database = client.get_database_client("image-results")
        self.container = database.get_container_client("predictions")

    def post_result(self, label, confidence, filename):

        document = {
            "id": str(uuid.uuid4()),
            "prediction_label": label,
            "filename": filename,
            "confidence": float(confidence),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        self.container.create_item(body=document)
