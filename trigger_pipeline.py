import os
import requests
from base64 import b64encode
import json
import sys

def main():
    ado_org = os.getenv("INPUT_ADO_ORG")
    ado_project = os.getenv("INPUT_ADO_PROJECT")
    ado_pipeline_id = os.getenv("INPUT_PIPELINE_ID")
    ado_pat = os.getenv("INPUT_ADO_PAT")
    repo_ref_name = os.getenv("INPUT_REF_NAME")
    ado_api_version = os.getenv("INPUT_API_VERSION")

    if not all([ado_org, ado_project, ado_pipeline_id, ado_pat, repo_ref_name, ado_api_version]):
        print("Missing required environment variables")
        sys.exit(1)

    print(f"Parameters:")
    print(f"ADO Org = {ado_org}")
    print(f"ADO Project = {ado_project}")
    print(f"Pipeline ID = {ado_pipeline_id}")
    print(f"Ref Name = {repo_ref_name}")
    print(f"API Version = {ado_api_version}")

    template_parameters_raw = os.getenv("INPUT_TEMPLATE_PARAMETERS", "{}")
    template_parameters = {}
    try:
        template_parameters = json.loads(template_parameters_raw) if template_parameters_raw else {}
    except json.JSONDecodeError:
        print("Invalid JSON for template parameters")
        sys.exit(1)

    if not template_parameters:
        print("No template parameters provided. 'template-parameters' input must not be empty.")
        sys.exit(1)

    print(f"Template Parameters = {json.dumps(template_parameters, indent=2)}")

    url = f"https://dev.azure.com/{ado_org}/{ado_project}/_apis/pipelines/{ado_pipeline_id}/runs?api-version={ado_api_version}"

    headers = {
        "Content-Type": "application/json"
    }
    auth = b64encode(f":{ado_pat}".encode()).decode()
    headers["Authorization"] = f"Basic {auth}"

    payload = {
        "resources": {
            "repositories": {
                "self": {
                    "refName": repo_ref_name
                }
            }
        },
        "templateParameters": template_parameters
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        response_json = response.json()
        print("Response JSON:")
        print(json.dumps(response_json, indent=2))
    except ValueError:
        print("Response Text:")
        print(response.text)

    if response.status_code != 200:
        sys.exit(1)

if __name__ == "__main__":
    main()
