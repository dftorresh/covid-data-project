import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from utility import get_configs_from_file, download_file


def ingest_file_into_azure_storage(
    local_file_path,
    storage_account_url,
    az_credentials,
    container_name
):
    blob_service_client = BlobServiceClient(
        f"{storage_account_url}", credential=az_credentials)
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=os.path.basename(local_file_path)
    )
    with open(local_file_path, 'rb') as data:
        blob_client.upload_blob(data)


# def testtt():
az_resources_config_file = os.path.join(
    os.path.dirname(__file__), 'az_resources_info.txt')
az_config = get_configs_from_file(az_resources_config_file)
storage_account_link = az_config['storage_account_url']
azure_credentials = DefaultAzureCredential()
container_name = 'raw'

hospital_data_file_url = "https://opendata.ecdc.europa.eu/covid19/hospitalicuadmissionrates/csv/data.csv"
downloaded_file_temp_path = '/opt/airflow/tasks/hospital_admissions.csv'
download_file(
    web_file_url=hospital_data_file_url,
    target_folder=downloaded_file_temp_path
)

ingest_file_into_azure_storage(
    local_file_path=downloaded_file_temp_path,
    storage_account_url=storage_account_link,
    az_credentials=azure_credentials,
    container_name='raw'
)
os.remove(downloaded_file_temp_path)

container_name = 'lookup'
ingest_file_into_azure_storage(
    local_file_path='/opt/airflow/tasks/data_ingestion/utility_data/country_lookup.csv',
    storage_account_url=storage_account_link,
    az_credentials=azure_credentials,
    container_name=container_name
)

ingest_file_into_azure_storage(
    local_file_path='/opt/airflow/tasks/data_ingestion/utility_data/dim_date.csv',
    storage_account_url=storage_account_link,
    az_credentials=azure_credentials,
    container_name=container_name
)
