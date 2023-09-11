# Airflow Starter Kit

This is a starter kit for executing scheduled dbt runs (Bolt schedules) within Apache Airflow. For ease of deployment, this project uses Astronomer.io to manage Apache Airflow. If you want to deploy your project locally, see the section below titled "Deploy Your Project Locally Using Astronomer."

## Table of Contents

- [Prerequisites](#prerequisites)
- [Instructions](#instructions)
   - [Step 1: Generate an API Key in Paradime](#step-1-generate-an-api-key-in-paradime)
   - [Step 2: Add Variables to Airflow](#step-2-add-variables-to-airflow)
   - [Step 3: Add Python Files to Your DAGs Folder](#step-3-add-python-files-to-your-dags-folder)
   - [Step 4: Update Variables in dags.py](#step-4-update-variables-in-dagspy)
   - [Step 5: Save the Updated dags.py File](#step-5-save-the-updated-dagspy-file)
   - [Step 6: Test and Deploy Your DAGs](#step-6-test-and-deploy-your-dags)
- [Details of Each Python File](#details-of-each-python-file)
   - [dags.py](#1-dagspy)
   - [paradime_schedules.py](#2-paradime_schedulespy)

## Prerequisites

Before using this starter kit, ensure you have the following prerequisites set up:

1. An existing airflow project
2. An Integrated Development Environment (IDE) like VSCode
3. Docker, Podman, or a similar tool
4. Python

This demo doesn't cover the initial setup of an Airflow project. If you need guidance on setting up an Airflow project, sign up for a free trial of astronomer.io and follow their instructions.

## Instructions

Follow these steps to set up and run your scheduled dbt runs with Paradime and Apache Airflow:

1. Generate a new API key in Paradime by clicking "Generate API Key" in the [Paradime account settings](https://app.paradime.io/account-settings/workspace). Here's what it looks like:

![image](https://github.com/jpooksy/demo-astro-project/assets/107123308/c908ee15-9db7-49e2-aa44-9a91fdf70ed5)


2. Add the following variables to your Airflow deployment:

   - `X-API-KEY`
   - `X-API-SECRET`
   - `URL`

   The values of these variables should be the values you generated in Paradime (step 1)
   <img width="1454" alt="image" src="https://github.com/jpooksy/demo-astro-project/assets/107123308/6eacdef2-c6cd-4e95-b5eb-b2f3cb856510">


   Note: 
   - If you are running airflow locally (ex. through Docker or Podmam) your airflow deployment URL might look something like: http://localhost:8080
   - If you are running airflow in the cloud (ex. through astronomer) your arflow deployment URL might look something like: sadflsdf000101getpnvrhv8.astronomer.run/d4rf5zb8

3. Add the following Python files to your Airflow "dags" folder:

   - `dags.py`
   - `paradime_schedules.py`

4. In the `dags.py` file, update the following variables:

   - `DAG_ID`: A unique identifier for the DAG (e.g., `DAG_ID = "0_bolt_airflow"`).
   - `DAG_INTERVAL`: A cron schedule for when the DAG should run (e.g., `DAG_INTERVAL = "@daily"`).
   - `SCHEDULE_NAME`: Should match the name of the schedule in `paradime_schedules.yml` in the DBT folder (e.g., `SCHEDULE_NAME = "my_schedule_name_in_paradime"`).
     
5. Save the updated `dags.py` file.

6. Test and deploy your new scheduled dbt runs. Depending on your Airflow setup, you can test your new DAGs. For example, if you're using Astronomer, you can use the following command:
   - Astro example: astro deploy --dags
   - Here's what I looks like in the Airflow UI:
      <img width="1507" alt="image" src="https://github.com/jpooksy/demo-astro-project/assets/107123308/3ca5750c-4b7c-4935-aef3-14c944bc3ed6">


## Details of Each Python File

### 1. dags.py

This Python file, `dags.py`, provides an example setup for running Paradime's Bolt within an Apache Airflow Directed Acyclic Graph (DAG). It demonstrates how to configure Airflow to interact with Paradime's API for scheduling and monitoring tasks. To use this DAG, Airflow needs specific variables such as `X-API-KEY`, `X-API-SECRET`, and `URL`. Additionally, you can customize global variables within the file, including `DAG_ID`, `DAG_INTERVAL`, and `SCHEDULE_NAME`.

The main components and actions performed in this DAG include:

- Importing required modules and functions from Apache Airflow and Paradime.
- Defining global variables like `DAG_ID`, `DAG_INTERVAL`, and `SCHEDULE_NAME`.
- Creating an Airflow DAG object with the specified configuration.
- Defining Airflow tasks, including start and end tasks (represented by DummyOperator), upstream and downstream tasks (using BashOperator and PythonOperator), and a Python sensor (PythonSensor) to monitor the status of a Bolt run.
- Configuring the task dependencies, where tasks are executed sequentially.

This example serves as a template for incorporating Paradime's Bolt into custom Airflow workflows for scheduling and automating tasks. Users can modify this DAG to fit their specific requirements and integrate it into their Airflow environment.

Remember to replace the variable values and schedule name according to your Paradime setup and use case before deploying this DAG.

### 2. paradime_schedules.py

The `paradime_schedules.py` Python script provides essential functions for interacting with Paradime's scheduling API within an Apache Airflow environment. It facilitates the execution and monitoring of scheduled tasks through the following functions:

- `run_schedule(schedule_name: str, task_instance: TaskInstance) -> None`: This function triggers the execution of a Paradime Bolt run using a GraphQL mutation query. It accepts the `schedule_name` as a parameter and communicates with the Paradime API by sending a POST request. The resulting `run_id` is extracted from the API response and stored in the Airflow task instance's XCom data for tracking.

- `get_run_status(task_instance: TaskInstance) -> bool`: This function retrieves the status of a previously triggered Paradime Bolt run. It queries the Paradime API for the run's status using the `run_id` stored in the task instance's XCom data. The function raises exceptions if the run has failed or encountered errors and returns `True` if the run is not in a "RUNNING" state.

- `_extract_gql_response(request: requests.Response, query_name: str, field: str) -> str`: A utility function used internally to extract relevant data from the GraphQL API response. It handles parsing and error checking.

To use these functions effectively, users must configure their Apache Airflow environment with the necessary variables such as `URL`, `X-API-KEY`, and `X-API-SECRET`. This script enables the integration of Paradime's scheduling capabilities into custom Airflow workflows for automated task execution and monitoring.
