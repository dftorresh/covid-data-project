FROM apache/airflow:2.5.1
USER root

RUN apt-get update \
    && apt-get -y install curl \
    # This line will install the Azure CLI inside the Airflow Containers
    && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash