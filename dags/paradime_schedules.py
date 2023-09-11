# Standard library modules
from typing import Union, Any

# Third party modules
from airflow.models.taskinstance import TaskInstance
from airflow.models import Variable
import requests

url = Variable.get("URL")
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": Variable.get("X-API-KEY"),
    "X-API-SECRET": Variable.get("X-API-SECRET"),
}

def run_schedule(schedule_name: str, task_instance: TaskInstance) -> None:
    query = """
    mutation trigger($scheduleName: String!) {
      triggerBoltRun(scheduleName: $scheduleName){
        runId
      }
    }
    """

    response = requests.post(
        url,
        json={"query": query, "variables": {"scheduleName": schedule_name}},
        headers=headers,
    )
    run_id = _extract_gql_response(response, "triggerBoltRun", "runId")

    # store run_id
    task_instance.xcom_push(key="run_id", value=run_id)


def get_run_status(task_instance: TaskInstance) -> bool:
    query = """
    query Status($runId: Int!) {
      boltRunStatus(runId: $runId) {
        state
      }
    }
    """

    run_id = task_instance.xcom_pull(key="run_id")
    response = requests.post(
        url, json={"query": query, "variables": {"runId": int(run_id)}}, headers=headers
    )
    state = _extract_gql_response(response, "boltRunStatus", "state")

    if state == "FAILED":
        raise Exception(f"Run {run_id} failed")
    elif state == "ERROR":
        raise Exception(f"Run {run_id} has error(s)")

    return state != "RUNNING"


def _extract_gql_response(
    request: requests.Response, query_name: str, field: str,
) -> str:
    response_json = request.json()
    if "errors" in response_json:
        raise Exception(f"{response_json['errors']}")

    try:
        return response_json["data"][query_name][field]
    except (TypeError, KeyError) as e:
        raise ValueError(f"{e}: {response_json}")