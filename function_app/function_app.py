import azure.functions as func
import logging
import image_predictor
import os

predictor = image_predictor.Predictor()
cosmos_handler = image_predictor.CosmosDB_handler()

app = func.FunctionApp()

@app.blob_trigger(arg_name="blob_data", path="input-images/{name}", connection="AzureWebJobsStorage")
def classify_image(blob_data : func.InputStream):
    
    logging.info(f"Processing blob {blob_data.name}. Size - {blob_data.length}")

    label, confidence = predictor.get_prediction(blob_data.read())
    logging.info(f"Blob {blob_data.name} classification complete. Label - {label}, Confidence {confidence}")
    
    filename = os.path.basename(blob_data.name)
    cosmos_handler.post_result(label, confidence, filename)
    logging.info(f"Blob {blob_data.name} classification results pushed to cosmosDB.")



