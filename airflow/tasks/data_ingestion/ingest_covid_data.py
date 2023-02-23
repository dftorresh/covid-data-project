import requests
import os
import shutil
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def get_az_resources_config(configs_file_path):
    resources_details = {}
    for line in open(configs_file_path):
        key, value = line.rstrip('\n').split(' = ')
        resources_details[key] = value[1:-1]
    return resources_details


def download_file(web_file_link, target_folder):
    r = requests.get(web_file_link, stream=True)
    with open(target_folder, "wb") as file:
        for chunk in r.iter_content(chunk_size=1024):
            # writing one chunk at a time to the file
            if chunk:
                file.write(chunk)


def upload_file_to_azure(local_file_path, storage_account_url, az_credentials, container_name):
    # blob_service_client = BlobServiceClient.from_connection_string(
    #     azure_storage_connection_string)
    blob_service_client = BlobServiceClient(f"{storage_account_url}",credential=az_credentials)
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=os.path.basename(local_file_path)
    )
    with open(local_file_path, 'rb') as data:
        blob_client.upload_blob(data)


def ingest_web_file_to_azure_storage(
    web_file_link,
    temp_local_file_path,
    storage_account_url,
    az_credentials,
    container_name
):
    download_file(
        web_file_link=web_file_link,
        target_folder=temp_local_file_path
    )
    upload_file_to_azure(
        local_file_path=temp_local_file_path,
        # azure_storage_connection_string=sa_connection_string,
        storage_account_url=storage_account_url,
        az_credentials=az_credentials,
        container_name=container_name
    )


temp_folder = './temp'
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

az_resources_config_file = os.path.join(os.path.dirname(__file__), '../../az_resources_info.txt')
# sa_connection_string = "DefaultEndpointsProtocol=https;AccountName=covidprojedb8db58sa;AccountKey=ksY/wS0VY2u/gIltQRVaIo2Bbu5mJLEQIIfdZFbCiWNO7J4qpLuysjHPBA9ooVEYd7s3P7rmY+Bi+AStyZpX5w==;EndpointSuffix=core.windows.net"
az_config = get_az_resources_config(az_resources_config_file)
storage_account_link = az_config['storage_account_url']
azure_credentialss = DefaultAzureCredential()
container_name = 'raw'
file_url = "https://opendata.ecdc.europa.eu/covid19/hospitalicuadmissionrates/csv/data.csv"
save_path = "./temp/hosp_data.csv"

# Ingest the actual file into az storage account.

ingest_web_file_to_azure_storage(
    web_file_link=file_url,
    temp_local_file_path=save_path,
    storage_account_url=storage_account_link,
    az_credentials=azure_credentialss,
    container_name=container_name
)

# container_name = 'lookup'
# upload_file_to_azure(
#     local_file_path='./airflow/tasks/data_ingestion/utility_data/country_lookup.csv',
#     azure_storage_connection_string=sa_connection_string,
#     container_name=container_name
# )

# upload_file_to_azure(
#     local_file_path='./airflow/tasks/data_ingestion/utility_data/dim_date.csv',
#     azure_storage_connection_string=sa_connection_string,
#     container_name=container_name
# )

if os.path.exists(temp_folder):
    shutil.rmtree(temp_folder, ignore_errors=False)
