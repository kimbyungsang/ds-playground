from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'start_date':days_ago(1),
    'catchup': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

templated_command = """
echo "ds: {{ dag_run.conf.ds }}"
"""

with DAG(
    'atest_dag_run_with_config',
    default_args=default_args,
    schedule_interval=None,
) as dag:

    t1 = BashOperator(
        task_id='with_config',
        bash_command=templated_command,
    )

t1