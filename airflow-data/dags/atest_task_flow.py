from airflow.decorators import dag, task
from airflow.operators.email import EmailOperator
from datetime import datetime
from typing import Dict
import requests
import logging

API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"

@dag(
    schedule_interval='@daily',
    start_date=datetime(2022, 12, 6),
    catchup=False,
)
def atest_task_flow():
    @task(task_id='extract', retries=2)
    def extract_bitcoin_price():
        return requests.get(API).json()['bitcoin']

    @task(multiple_outputs=True)
    def process_data(response):
        logging.info(response)
        return {'usd': response['usd'], 'change': response['usd_24h_change']}

    @task()
    def store_data(data):
        logging.info(f"stored data is {data['usd']} and with change {data['change']}")

    email_notification = EmailOperator(
        task_id='email_notification',
        to='kim.byung.sang@gmail.com',
        subject='bitcoin price with task flow',
        html_content='empty'
    )

    store_data(process_data(extract_bitcoin_price())) >> email_notification

dag = atest_task_flow()


