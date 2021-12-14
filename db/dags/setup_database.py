import datetime as dt

from scripts import setup_indices, setup_genes

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

def setup_go():
    print('Setting up GO nodes in database...')

def setup_gene():
    print('Setting up gene nodes in database...')

def setup_disease():
    print('Setting up disease nodes in database...')

def setup_efetch():
    print('Performing eFetch search...')


default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2021, 11, 10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('setup_database',
         default_args=default_args,
         schedule_interval='0 * * * *',
         ) as dag:

    setup_indices_operator = PythonOperator(task_id='setup_indices_task',
                                 python_callable=setup_indices.setup_indices)
    sleep = BashOperator(task_id='sleep1',
                         bash_command='sleep 5')
    setup_go_operator = PythonOperator(task_id='setup_go',
                                 python_callable=setup_go)
    sleep = BashOperator(task_id='sleep2',
                         bash_command='sleep 5')
    setup_gene_operator = PythonOperator(task_id='setup_gene',
                                 python_callable=setup_genes.setup_genes)
    sleep = BashOperator(task_id='sleep3',
                         bash_command='sleep 5')
    setup_disease_operator = PythonOperator(task_id='setup_disease',
                                 python_callable=setup_disease)
    sleep = BashOperator(task_id='sleep4',
                         bash_command='sleep 5')
    setup_efetch_operator = PythonOperator(task_id='setup_efetch',
                                 python_callable=setup_efetch)