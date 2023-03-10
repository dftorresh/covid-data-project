resource "azurerm_storage_account" "sa" {
    name = "covidproj${random_id.unique_identifier.hex}sa"
    resource_group_name = azurerm_resource_group.rg.name
    location = var.location
    account_tier = "Standard"
    account_replication_type = "LRS"
    account_kind = "StorageV2"
    is_hns_enabled = true
    allow_blob_public_access = true
}

resource "azurerm_storage_container" "raw_data_container" {
    name = var.raw_data_container_name
    storage_account_name = azurerm_storage_account.sa.name
    container_access_type = "blob"
}

resource "azurerm_storage_container" "processed_data_container" {
    name = var.processed_data_container_name
    storage_account_name = azurerm_storage_account.sa.name
    container_access_type = "blob"
}

resource "azurerm_storage_container" "lookup_data_container" {
    name = var.lookup_data_container_name
    storage_account_name = azurerm_storage_account.sa.name
    container_access_type = "blob"
}

resource "azurerm_role_assignment" "contributor_role" {
  scope                = azurerm_storage_account.sa.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azuread_service_principal.service_principal.id
}