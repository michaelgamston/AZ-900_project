# AZ-900_project

This project is combine with my studying for Azure's AZ-900 general cloud computing certificate. 

I have three aims for the project: 
- Develop my infrastructure-as-code skills by deploying cloud resources using terraform.
- Develop my knowledge of Azure's cloud resources and how I implement them.
-  Combine my existing development knowledge to complete full cloud based project within a new ecosystem.

My goal is to successfully build a image prediction pipeline following the structure detailed below.

API -> Azure Blob Storage -> Azure function (Image classifier) -> CosmoDB

Lastest push: 
- I've deployed a cosmosDB account and container and provisioned my account to have read/ write access to it. 
- I have also updated the image_predictor file to classify and image locally and then push the results in a JSON doc to the cosmosDB container

Next update: 
- I will deploy an Azure Function
- Update the image_predictor code so it is able run in the function, recieve images from Blod storage and then push the results to comsmosDB
