from airflow.decorators import dag, task
from datetime import datetime

@task()
def add_task(x, y):
    print(f'Task args {x} and {y}')
    return x + y

@dag(start_date=datetime(2022,12,6))
def mydag():
    start = add_task.override(task_id="start")(1, 2)
    for i in range(3):
        start >> add_task.override(task_id=f'add_start_{i}')(start, i)

@dag(start_date=datetime(2022,12,6))
def mydag2():
    start = add_task(1, 2)
    for i in range(3):
        start >> add_task.override(task_id=f'new_added_start_{i}')(start, i)

first_dag = mydag()
second_dag = mydag2()
