terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.88.0"
    }
  }
}

provider "azurerm" {
  skip_provider_registration = "true"
  features {

  }
}

data "azurerm_client_config" "current" {}

resource "azurerm_storage_account" "storage" {
  name                              = "storagezoomcamp"
  resource_group_name               = var.rg_name
  location                          = var.rg_location
  account_tier                      = "Standard"
  account_replication_type          = "GRS"
  account_kind                      = "StorageV2"
  is_hns_enabled                    = "true"
  tags = {
    environment = "development"
    source      = "terraform"
  }
}

resource "azurerm_storage_data_lake_gen2_filesystem" "fs" {
  name               = "synapse"
  storage_account_id = azurerm_storage_account.storage.id
}

resource "azurerm_synapse_workspace" "synapse" {
  name                                 = "synapse-zoomcamp"
  resource_group_name                  = var.rg_name
  location                             = "westus"
  storage_data_lake_gen2_filesystem_id = azurerm_storage_data_lake_gen2_filesystem.fs.id
  sql_administrator_login              = "sqladminuser"
  sql_administrator_login_password     = "root@5963"

  aad_admin {
    login     = "AzureAD Admin"
    object_id = data.azurerm_client_config.current.object_id
    tenant_id = data.azurerm_client_config.current.tenant_id
  }
  identity {
    type = "SystemAssigned"
  }
  tags = {
    environment = "development"
    source      = "terraform"
  }
}
