import json
import os
import time
import traceback

import functions_framework
import requests
from flask import abort

headers = {"Authorization": f"token {os.getenv('PERSONAL_TOKEN')}"}


@functions_framework.http
def main(request):
    try:
        if "owner" not in request.args or "repo" not in request.args:
            return abort(400, "'owner' and 'repo' are required'")
        owner = request.args.get("owner")
        repo_name = request.args.get("repo")
        data_v4 = fetch_api_v4(owner, repo_name)
        print(data_v4)
    except Exception as e:
        print(f"Trace: {traceback.format_exc()}")
        time.sleep(5)
        raise e
    return ""


def fetch_api_v4(owner: str, repo_name: str):
    url = "https://api.github.com/graphql"
    query = {
        "query": "query {  "
        + '     repository(name: "'
        + repo_name
        + '", owner: "'
        + owner
        + '") { '
        + "       forkCount "
        + "       pullRequests { totalCount } "
        + "       stargazers { totalCount } "
        + "       issues { totalCount } "
        + "       releases { totalCount } "
        + "       watchers { totalCount } "
        + "}}"
    }

    response = requests.post(url, json=query, headers=headers)

    if 200 < response.status_code < 300:
        return json.dumps(response.json())
    else:
        raise Exception(
            f"Query failet to run by returning code of {response.status_code, query}"
        )


def fetch_api_v3(owner: str, repo_name: str, path: str):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/{path}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if 200 < response.status_code < 300:
        return data
    else:
        raise Exception(
            f"Query failet to run by returning code of {response.status_code, query}"
        )
