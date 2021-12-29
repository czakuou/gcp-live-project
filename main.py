import json
import os
import time
import traceback

import functions_framework
import requests
from dotenv import load_dotenv
from flask import abort

load_dotenv()


def main(request):
    try:
        if "owner" not in request.args or "repo" not in request.args:
            return abort(400, "'owner' and 'repo' are required'")

        owner = request.args["owner"]
        repo_name = request.args["repo_name"]

        data_v4 = fetch_api_v4(owner, repo_name)
        print(data_v4)

        stat = fetch_api_v3(owner, repo_name, "stats/contributors")
        print(stat)

        commits = fetch_api_v3(owner, repo_name, "commits")
        print(commits)

        pr = fetch_api_v3(owner, repo_name, "pulls?state=all")
        print(pr)

        issues = fetch_api_v3(owner, repo_name, "issues?state=all")
        print(issues)

    except Exception as e:
        print(f"Trace: {traceback.format_exc()}")
        time.sleep(5)
        raise e

    return ""


def fetch_api_v4(owner: str, repo_name: str):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"token {os.environ.get('PERSONAL_TOKEN')}"}

    query = {
        "query": "{  "
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

    if 200 <= response.status_code < 300:
        return json.dumps(response.json())
    else:
        raise Exception(
            f"Query failed to run by returning code of {response.status_code, query}"
        )


def fetch_api_v3(owner: str, repo_name: str, path: str):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/{path}"

    headers = {"Authorization": f"token {os.environ.get('PERSONAL_TOKEN')}"}

    objects = []
    while url is not None:
        response = requests.get(url, headers=headers)

        if 200 <= response.status_code < 300:
            data = response.json()
            for record in data:
                objects.append(json.dumps(record))
            print(response.headers)
            url = None
            if "link" in response.headers:
                for link in response.headers["link"].split(","):
                    if "next" in link:
                        url = link.split(";")[0].strip("<> ")
                        break
        else:
            raise Exception(
                f"Query failed to run by returning code of {response.status_code}"
            )

    return objects
