# AZ-900_project

This project is combine with my studying for Azure's AZ-900 general cloud computing certificate. 

I have three aims for the project: 
- Develop my infrastructure-as-code skills by deploying cloud resources using terraform.
- Develop my knowledge of Azure's cloud resources and how I implement them.
-  Combine my existing development knowledge to complete full cloud based project within a new ecosystem.

My goal is to successfully build a image prediction pipeline following the structure detailed below.

API -> Azure Blob Storage -> Azure function (Image classifier) -> CosmoDB

Lastest push: 
- function_app/function_app.py code created and tested locally
- image_predictor.py refactor to be module ready
- function_app deployed and running in azure

Next update: 
- refactor code to handle fail cases and seal up vulnerabilities
- write some code tests 
