import json
from datetime import datetime
from textwrap import dedent

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {'owner': 'airflow',}

with DAG(
    'etl_dag',
    default_args=default_args,
    description='etl example lagacy',
    schedule_interval=None,
    start_date=datetime(2022,12,6),
    catchup=False,
    tags=['examples']
) as dag:
    dag.doc_md = __doc__


    def extract(**kwargs):
        ti = kwargs['ti']
        data_string = {'1001': 301.27, '1002': 433.21, '1003': 502.22}
        ti.xcom_push('order_data', data_string)

    def transform(**kwargs):
        ti = kwargs['ti']
        extract_data_string = ti.xcom_pull(task_ids='extract', key='order_data')

        total_order_value = 0
        for value in extract_data_string.values():
            total_order_value += value

        total_value = {'total_order_value': total_order_value}
        total_value_json_string = json.dumps(total_value)
        ti.xcom_push('total_order_value', total_value_json_string)

    def load(**kwargs):
        ti = kwargs['ti']
        total_value_string = ti.xcom_pull(task_ids='transform', key='total_order_value')
        total_order_value = json.loads(total_value_string)
        print(total_order_value)


    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    abcd 
    efg 
    """
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    transform_task.__doc__ = dedent(
        """
        #TRANSFORM task will be described..!
        """
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,

    )

    load_task.__doc__ = dedent(
        """
        #LOAD task will be described..!
        """
    )

    extract_task >> transform_task >> load_task