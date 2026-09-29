import io
import os
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobBlock, BlobClient, StandardBlobTier

class uploader:

    def __init__(self):
        account_url = "https://az900images.blob.core.windows.net"
        credential = DefaultAzureCredential()
        # Create the BlobServiceClient object
        self.blob_service_client = BlobServiceClient(account_url, credential=credential)

        print("Account:", self.blob_service_client.account_name)

        for container in self.blob_service_client.list_containers():
            print("Container:", container.name)

    def upload_blob_file(self, file_pth : str, container_name = "input-images"):
        
        container_client = self.blob_service_client.get_container_client(container=container_name)
        blob_name = os.path.basename(file_pth)

        with open(file=file_pth, mode="rb") as data:
            blob_client = container_client.upload_blob(name=blob_name, data=data, overwrite=True)
        
uploader().upload_blob_file("../images/Screenshot from 2025-05-06 16-35-53.png")