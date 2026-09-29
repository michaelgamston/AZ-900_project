#list the providers that will be used 

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 5.0"
    }
  }
}

provider "azurerm" {
  features {}
}

#create a resource group to organise our resources
resource "azurerm_resource_group" "AZ900" {
  name     = "AZ900_project"
  location = "UK South"
}


#------------
#Storage blob
#------------


#storage account
resource "azurerm_storage_account" "AZ900" {
  name                     = "az900images"
  resource_group_name      = azurerm_resource_group.AZ900.name
  location                 = azurerm_resource_group.AZ900.location

  account_tier             = "Standard"
  account_replication_type = "LRS"
}

#blob container to hold individual blobs
resource "azurerm_storage_container" "input" {
  name                  = "input-images"
  storage_account_id  = azurerm_storage_account.AZ900.id
  container_access_type = "private"
}

#give my account permission to upload to blob
#id stored in variables.tf not uploaded to git
resource "azurerm_role_assignment" "blob_contributor" {
  scope                 = azurerm_storage_account.AZ900.id
  role_definition_name  = "Storage Blob Data Contributor"
  principal_id          = var.blob_contributor_id
}


#------------
#Cosmo db
#------------

# resource "azurerm_cosmosdb_account" "AZ900" {
#   name                = "AZ900results"
#   location            = azurerm_resource_group.AZ900.location
#   resource_group_name = azurerm_resource_group.AZ900.name

#   offer_type = "Standard"
#   kind       = "GlobalDocumentDB"

#   consistency_policy {
#     consistency_level = "Session"
#   }

#   geo_location {
#     location          = azurerm_resource_group.main.location
#     failover_priority = 0
#   }
# }

# resource "azurerm_cosmosdb_sql_database" "AZ900" {
#   name                = "image-results"
#   resource_group_name = azurerm_resource_group.main.AZ900
#   account_name        = azurerm_cosmosdb_account.main.AZ900
# }

# resource "azurerm_cosmosdb_sql_container" "predictions" {
#   name                = "predictions"
#   resource_group_name = azurerm_resource_group.AZ900.name
#   account_name        = azurerm_cosmosdb_account.AZ900.name
#   database_name       = azurerm_cosmosdb_sql_database.AZ900.name

#   partition_key_paths = ["/imageId"]
# }

# #------------
# #Azure Function
# #------------

# resource "azurerm_service_plan" "AZ900" {
#   name                = "image-pipeline-plan"
#   resource_group_name = azurerm_resource_group.AZ900.name
#   location            = azurerm_resource_group.AZ900.location

#   os_type  = "Linux"
#   sku_name = "Y1"
# }

# resource "azurerm_linux_function_app" "AZ900" {
#   name                = "process_images_post_results"
#   resource_group_name = azurerm_resource_group.AZ900.name
#   location            = azurerm_resource_group.AZ900.location

#   service_plan_id = azurerm_service_plan.AZ900.id

#   storage_account_name       = azurerm_storage_account.AZ900.name
#   storage_account_access_key = azurerm_storage_account.AZ900.primary_access_key

#   site_config {
#     application_stack {
#       python_version = "3.11"
#     }
#   }
# }