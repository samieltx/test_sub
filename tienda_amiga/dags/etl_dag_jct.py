from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

from tienda_amiga.extract import get_news_from_api
from tienda_amiga.load import load_to_postgres
from tienda_amiga.transform_jct import transform

with DAG(    
        dag_id='gnews_bitcoin_dag',
        start_date=datetime(2023, 5, 12),
        schedule_interval=None,        
    ) as dag:
    dummy_start_task = DummyOperator(task_id="dummy_start")

    def _print_execution_date(ds):
        print(f"The execution date of this flow is {ds}")

    print_dag = PythonOperator(
        task_id='print_task',
        python_callable=_print_execution_date,
        dag=dag,
    )

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=get_news_from_api,
        op_args=["bitcoin"],
    )

    # TODO: Code transform task (for example you can use pandas)
    transform_task = PythonOperator(
        task_id="transform_jct",
        python_callable=transform,
    )

    # TODO: Code load task (for example you can use SQLAlchemy)
    load_task = PythonOperator(
        task_id="load",
        python_callable=load_to_postgres,
        op_args=["bitcoin"],
    )

    dummy_end_task = DummyOperator(task_id="dummy_end")

    dummy_start_task >> extract_task >> transform_task >> load_task >> print_dag >> dummy_end_task