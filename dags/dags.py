# Example setup for running Paradime's Bolt in your own airflow DAG
#
# Airflow will need to be set up with the variables
# find these variables by clicking "Generate API Key" here: https://app.paradime.io/account-settings/workspace
# - X-API-KEY
# - X-API-SECRET
# - URL
#
# The global variables should also be customized in this file:
# - DAG_ID - a unique identifier for the DAG
# - DAG_INTERVAL - a cron schedule for when the DAG should run (e.g., "0 0 * * *")
# 
# - SCHEDULE_NAME - should match the name of the "name" field
#   in the paradime_schedules.yml file in the DBT folder

# Standard library modules
import datetime

# Third-party modules

# Airflow specific imports
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.python import PythonSensor

# Import Paradime functions
from paradime_schedules import run_schedule, get_run_status

# Give an ID to your DAG - this is required by Airflow
# You can leave the name as is, or you can change it to whatever you'd like
# Example: change the DAG_ID value from "0_bolt_airflow" to "paradime_bolt_schedule_airflow"
DAG_ID = "0_bolt_airflow"

# This is the interval at which the DAG should run
# Because the run is now triggered from Airflow through API,
# the cron schedule in paradime_schedules.yaml does not matter 
DAG_INTERVAL = "@daily"

# This is the schedule name that you want to run - the name
# should match the schedule name in paradime_schedules.yaml
# Example: change the DAG_ID value from "my_schedule_name_in_paradime" to "dbt_scheduled_runs"
SCHEDULE_NAME = "dbt_scheduled_runs"

with DAG(
    dag_id=DAG_ID,
    schedule_interval=DAG_INTERVAL,
    default_args={
        "start_date": datetime.datetime.today() - datetime.timedelta(days=1),
    },
    catchup=False,
) as dag:
    start = DummyOperator(task_id="start")

    # Some Airflow upstream tasks - here we are using the BashOperator
    # can be replaced by your company-specific task
    upstream_task = BashOperator(
        task_id="example_data_ingestion_task",
        bash_command='echo "running some task for data ingestion"',
    )

    bolt_schedule_run = PythonOperator(
        task_id=f"start_schedule_run_{SCHEDULE_NAME.replace(' ', '_')}",
        python_callable=run_schedule,
        op_args=[SCHEDULE_NAME],  # Pass arguments as positional arguments
    )

    bolt_get_run_status = PythonSensor(
        task_id=f"get_run_status_{SCHEDULE_NAME.replace(' ', '_')}",
        python_callable=get_run_status,
    )

    # Some Airflow tasks after bolt run - here we are using the BashOperator
    # can be replaced by your company-specific tasks
    downstream_task = BashOperator(
        task_id="example_data_upload_task",
        bash_command='echo "running some task after bolt run"',
    )

    end = DummyOperator(task_id="end")

    (start >> upstream_task >> bolt_schedule_run >> bolt_get_run_status >> downstream_task >> end)
