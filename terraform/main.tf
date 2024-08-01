# Azure Provider source and version being used
terraform {
    required_version = "~>1.9.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
   }
  }
  backend "azurerm" {
      resource_group_name  = "flask-app"
      storage_account_name = "tfstateflaskapp"
      container_name       = "tfstateflaskapp"
      key                  = "terraform.tfstate"
  }

}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "flask-app" {
  name     = "flask-app"
  location = "UK South"
  tags     = {environment="development"}
}

#For tf state storage
resource "azurerm_storage_account" "tfstate" {
  name                     = "tfstateflaskapp"
  resource_group_name      = azurerm_resource_group.flask-app.name
  location                 = azurerm_resource_group.flask-app.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  allow_nested_items_to_be_public = false

  tags = {
    environment = "development"
  }
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstateflaskapp"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "private"
}