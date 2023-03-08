output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "storage_account_url" {
  value = azurerm_storage_account.sa.primary_blob_endpoint
  description = "Primary blob endpoint of the storage account"
}