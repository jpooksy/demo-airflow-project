Airflow Starter Kit
========

This is a starter kit for executing scheduled dbt runs (Bolt schedules) within Apache Airflow. For ease of deployment, this project uses Astronomer.io to manage Apache Airflow

## Instructions

1: Within Paradime, generage a new API key by clicking "Generate API Key" in the [Paradime account settings](https://app.paradime.io/account-settings/workspace)

Here's what it looks like: 
![image](https://github.com/jpooksy/demo-astro-project/assets/107123308/c908ee15-9db7-49e2-aa44-9a91fdf70ed5)


2: Navitate to your Airflow deployment and add the following variables:

   - `X-API-KEY`
   - `X-API-SECRET`
   - `URL`

The values of these variables should be the values you generated in Paradime (step 1)
<img width="1454" alt="image" src="https://github.com/jpooksy/demo-astro-project/assets/107123308/6eacdef2-c6cd-4e95-b5eb-b2f3cb856510">

Note: 
- If you are running airflow locally (ex. through Docker or Podmam) your airflow deployment URL might look something like: http://localhost:8080
- If you are running airflow in the cloud (ex. through astronomer) your arflow deployment URL might look something like: sadflsdf000101getpnvrhv8.astronomer.run/d4rf5zb8



2: You have an exisiting Airflow project (This project uses Astronomer.io to manage Apache Airflow)

## Instructions

1: Add the following files to your "dags" folder
- `dags.py`
- `paradime_schedules.py`

2: within the `dags.py` file, update the following variables
- `DAG_ID`: A unique identifier for the DAG.
- `DAG_INTERVAL`: A cron schedule for when the DAG should run (e.g., "0 0 * * *").
- `SCHEDULE_NAME`: Should match the name of the schedule in `paradime_schedules.yml` in the DBT folder.



This repository provides the necessary python files to execute schedule dbt runs in Apache Airflow, including:

1: **dags.py: **this file sets up an Airflow DAG that automates the triggering and monitoring of Paradime Bolt runs as part of a larger data pipeline. The configuration is customizable, and it demonstrates how to integrate Paradime's functionality into an Airflow workflow for data processing and automation. 

The file provides instructions on how to set up the necessary environment variables for Airflow. Specifically, it mentions that you need to configure the following variables: 
- `X-API-KEY`
- `X-API-SECRET`
- - `URL`

You can custominze the following variables in your DAG configuration:

Customize the following variables in your DAG configuration:

- `DAG_ID`: A unique identifier for the DAG.
- `DAG_INTERVAL`: The cron schedule for the DAG (e.g., "@daily").
- `SCHEDULE_NAME`: Should match the name of the schedule in paradime_schedules.yml.

These variables are typically obtained by generating an API key in Paradime's platform. You can generate an API key in you [Paradime account settings](https://app.paradime.io/account-settings/workspace)


2: paradime_schedules.py




Project Contents
================

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes two example DAGs:
    - `example_dag_basic`: This DAG shows a simple ETL data pipeline example with three TaskFlow API tasks that run daily.
    - `example_dag_advanced`: This advanced DAG showcases a variety of Airflow features like branching, Jinja templates, task groups and several Airflow operators.
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

2. Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#ports-are-not-available).

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://docs.astronomer.io/cloud/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support.
