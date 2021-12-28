import requests
import functions_framework
import os
import json


headers = {"Authorization": f"token {os.getenv('PERSONAL_TOKEN')}"}


@functions_framework.http
def run_fetch(request):
    data = fetch_api_v4("facebook", "graphql")
    return data


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


# def fetch_api_v3(owner: str, repo_name: str, path: str):
#     url = f"https://api.github.com/repos/{owner}/{repo_name}/{path}"
#     response = requests.get(url, headers=headers)
#     data = response.json()
#     if response.status_code == 200:
#         return data
#     else:
#         raise Exception(
#             f"Query failet to run by returning code of {response.status_code, query}"
#         )
