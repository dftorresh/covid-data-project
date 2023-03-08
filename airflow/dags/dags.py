from airflow import DAG
from airflow.decorators import dag
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
# from airflow.operators.python import PythonOperator
# from airflow.tasks.data_ingestion.ingest_covid_data import testtt

start_time = days_ago(2)


# @dag(
#     start_date=start_time,
#     catchup=False,
#     schedule_interval='@daily',
#     max_active_runs=1
# )
# def print_hello_dag():
#     print('hello')


# dag = print_hello_dag()
with DAG(
    'covid_data_processing',
    start_date=start_time,
    catchup=False,
    schedule_interval='@daily',
    max_active_runs=1
) as dag:
    data_scraper = BashOperator(
        task_id="data_ingestion",
        bash_command="python3 /opt/airflow/tasks/data_ingestion/ingest_covid_data.py"
    )

    data_scraper
