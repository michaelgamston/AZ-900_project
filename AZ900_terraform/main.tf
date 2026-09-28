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
resource "azurerm_resource_group" "main" {
  name     = "rg-image-pipeline"
  location = "UK South"
}


#------------
#Storage blob
#------------

#storage account
resource "azurerm_storage_account" "main" {
  name                     = "youruniquestorageaccount"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location

  account_tier             = "Standard"
  account_replication_type = "LRS"
}

#blob container to hold individual blobs
resource "azurerm_storage_container" "input" {
  name                  = "input-images"
  storage_account_id  = azurerm_storage_account.main.id
  container_access_type = "private"
}

#------------
#Cosmo db
#------------

resource "azurerm_cosmosdb_account" "main" {
  name                = "your-unique-cosmos-name"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  offer_type = "Standard"
  kind       = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_sql_database" "main" {
  name                = "image-results"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_cosmosdb_sql_container" "predictions" {
  name                = "predictions"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name

  partition_key_paths = ["/imageId"]
}

#------------
#Azure Function
#------------

resource "azurerm_service_plan" "main" {
  name                = "image-pipeline-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  os_type  = "Linux"
  sku_name = "Y1"
}

resource "azurerm_linux_function_app" "main" {
  name                = "your-unique-function-name"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  service_plan_id = azurerm_service_plan.main.id

  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }
}