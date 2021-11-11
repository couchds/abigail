import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

def setup_disease():
    print('Setting up disease nodes in database...')

default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2021, 11, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('setup_disease',
         default_args=default_args,
         schedule_interval='0 * * * *',
         ) as dag:

    sleep = BashOperator(task_id='sleep',
                         bash_command='sleep 5')
    print_world = PythonOperator(task_id='setup_disease',
                                 python_callable=setup_disease)