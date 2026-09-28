import io
import os
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobBlock, BlobClient, StandardBlobTier

#TODO: Replace <storage-account-name> with your actual storage account name
account_url = "https://az900images.blob.core.windows.net"
credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=credential)

def upload_blob_file(file_pth : str, blob_service_client = blob_service_client, container_name = "input-images"):
    
    container_client = blob_service_client.get_container_client(container=container_name)
    
    with open(file=file_pth, mode="rb") as data:
        blob_client = container_client.upload_blob(name=file_pth, data=data, overwrite=True)
        
upload_blob_file("images/Screenshot from 2025-05-06 16-35-53.png")