from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

from tienda_amiga.extract import get_news_from_api
from tienda_amiga.load import load_to_postgres
from tienda_amiga.transform import transform

with DAG(
        dag_id='gnews_covid_dag',
        start_date=datetime(2023, 3, 20),
        schedule_interval=None,
    ):
    dummy_start_task = DummyOperator(task_id="dummy_start")

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=get_news_from_api,
        op_args=["covid"],
    )

    # TODO: Code transform task (for example you can use pandas)
    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    # TODO: Code load task (for example you can use SQLAlchemy)
    load_task = PythonOperator(
        task_id="load",
        python_callable=load_to_postgres,
        op_args=["covid"],
    )

    dummy_end_task = DummyOperator(task_id="dummy_end")

    dummy_start_task >> extract_task >> transform_task >> load_task >> dummy_end_task