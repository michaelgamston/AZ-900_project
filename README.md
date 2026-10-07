# AZ-900_project

This project is combine with my studying for Azure's AZ-900 general cloud computing certificate. 

I have three aims for the project: 
- Develop my infrastructure-as-code skills by deploying cloud resources using terraform.
- Develop my knowledge of Azure's cloud resources and how I implement them.
-  Combine my existing development knowledge to complete full cloud based project within a new ecosystem.

My goal is to successfully build a image prediction pipeline following the structure detailed below.

API -> Azure Blob Storage -> Azure function (Image classifier) -> CosmoDB

Lastest push: 
- I've deployed a function 
- Created a local function_app folder to hold the function code
- Created a role for the function to allow it access to cosmosDB
- Given the function an app_setting to keep track of the cosmosDB endpoint

Next update: 
- update the function app code ready for deployment
- deploy the function app code to the function
