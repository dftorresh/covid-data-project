data "azurerm_subscription" "current" {
}

resource "random_id" "unique_identifier" {
  keepers = {
    susbscription_id = data.azurerm_subscription.current.subscription_id
  }
  byte_length = 4
}

variable "location" {
  default     = "eastus"
  description = "Location to be used for all the resources."
}

variable "resource_group_name" {
  default     = "covidj_data_project_rg"
  description = "Resource group where all the other resources will be created."
}

variable "storage_account_name" {
  default     = "fkdajflkdsajhd343"
  description = "Storage account where the data will be stored"
}

variable "raw_data_container_name" {
  default     = "raw"
  description = "Container where raw data will be stored"
}

variable "processed_data_container_name" {
  default     = "processed"
  description = "Container where the data will be stored after processing"
}

variable "lookup_data_container_name" {
  default     = "lookup"
  description = "Container containing some data used to enrich the covid dataset"
}

variable "data_factory_name" {
  default     = "df-covid-project-28"
  description = "Data Factory instance that will orchestrate ingestion and transformation data processes"
}

variable "databricks_name" {
  default     = "covid-project-dbws"
  description = "Databricks workspace where data transformation tasks will be created"
}

variable "databricks_cluster_name" {
  default     = "covid_data_processing_cl"
}

variable "cluster_note_type" {
  default="Standard_DS3_v2"
}

variable "cluster_num_workers" {
  type    = number
  default = 1
}

variable "cluster_autotermination_minutes" {
  type    = number
  default = 10
}

variable "service_principal_app_name" {
  default     = "covid-project-app"
}

variable "key_vault_name" {
  default     = "kv-covid-project28"
}

variable "sql_server_name" {
  default     = "sqlservercovidproject28"
}

variable "sql_database_name" {
  default     = "covid_data"
}
