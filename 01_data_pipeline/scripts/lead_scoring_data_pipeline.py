from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from dags import utils

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 2, 20),
    "retries": 1,
}

dag = DAG(
    "lead_scoring_data_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
)

task_1 = PythonOperator(
    task_id="build_dbs",
    python_callable=utils.build_dbs,
    dag=dag
)

task_2 = PythonOperator(
    task_id="load_data_into_db",
    python_callable=utils.load_data_into_db,
    dag=dag
)

task_3 = PythonOperator(
    task_id="map_city_tier",
    python_callable=utils.map_city_tier,
    dag=dag
)

task_4 = PythonOperator(
    task_id="map_categorical_vars",
    python_callable=utils.map_categorical_vars,
    dag=dag
)

task_1 >> task_2 >> task_3 >> task_4
