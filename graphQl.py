import requests
import time
import keyring
import os
import csv
from tqdm import tqdm

service_name = "GITHUB_API_TOKEN"
username = "LAB_EXPERIMENTACAO"

# Tenta obter o token do keyring
TOKEN = keyring.get_password(service_name, username)

# Se não achar no keyring, tenta na variável de ambiente
if not TOKEN:
    print("Token não encontrado no keyring. Tentando ler da variável de ambiente 'GITHUB_API_TOKEN'...")
    TOKEN = os.getenv("GITHUB_API_TOKEN")

if not TOKEN:
    raise ValueError("Tokenpython3 -m venv venv de autenticação não encontrado. Configure no keyring ou na variável de ambiente 'GITHUB_API_TOKEN'.")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
URL = "https://api.github.com/graphql"


def run_query(query, variables=None, retries=3):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    for attempt in range(retries):
        response = requests.post(URL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                raise Exception(f"GraphQL errors: {data['errors']}")
            return data
        elif response.status_code in [502, 503, 504]:
            print(f"Erro {response.status_code}, tentando novamente ({attempt+1}/{retries})...")
            time.sleep(5)
        else:
            raise Exception(f"Query failed: {response.status_code} {response.text}")

    raise Exception(f"Query failed after {retries} attempts")


def get_top_repo_ids(total_repos=1000):
    repos = []
    cursor = None
    per_page = 100  # GitHub GraphQL aceita até 100 por página

    while len(repos) < total_repos:
        query = """
        query($cursor: String, $perPage: Int!) {
          search(query: "stars:>1 sort:stars-desc is:public", type: REPOSITORY, first: $perPage, after: $cursor) {
            pageInfo { endCursor hasNextPage }
            edges {
              node {
                ... on Repository {
                  name
                  owner { login }
                }
              }
            }
          }
        }
        """
        variables = {"cursor": cursor, "perPage": per_page}
        result = run_query(query, variables)
        search = result["data"]["search"]

        for edge in search["edges"]:
            repos.append(edge["node"])
            if len(repos) >= total_repos:
                break

        if not search["pageInfo"]["hasNextPage"]:
            break
        cursor = search["pageInfo"]["endCursor"]

    return repos[:total_repos]


def get_repo_details(owner, name):
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        stargazerCount
        createdAt
        updatedAt
        primaryLanguage { name }
        releases { totalCount }
        issues(states: OPEN) { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
        pullRequests(states: MERGED) { totalCount }
      }
    }
    """
    variables = {"owner": owner, "name": name}
    result = run_query(query, variables)
    return result["data"]["repository"]


def collect_and_save_repo_data(filename="repos_data.csv"):
    repos = get_top_repo_ids(1000)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Owner", "Repository", "Stars", "Created At", "Last Updated",
            "Primary Language", "Releases", "Open Issues", "Closed Issues",
            "Closed Issues Ratio", "Merged Pull Requests"
        ])

        # Adicionando barra de progresso
        for repo in tqdm(repos, desc="Processando repositórios", unit="repo"):
            details = get_repo_details(repo["owner"]["login"], repo["name"])
            primary_language = details['primaryLanguage']['name'] if details['primaryLanguage'] else 'Unknown'
            open_issues = details['issues']['totalCount']
            closed_issues = details['closedIssues']['totalCount']
            total_issues = open_issues + closed_issues
            closed_ratio = (closed_issues / total_issues) if total_issues > 0 else 0

            writer.writerow([
                repo['owner']['login'],
                repo['name'],
                details['stargazerCount'],
                details['createdAt'],
                details['updatedAt'],
                primary_language,
                details['releases']['totalCount'],
                open_issues,
                closed_issues,
                f"{closed_ratio:.2f}",
                details['pullRequests']['totalCount']
            ])

    print(f"\n✅ Dados salvos em {filename}")


if __name__ == "__main__":
    start_time = time.time()
    collect_and_save_repo_data("repos_data.csv")
    print(f"⏱️ Tempo total de execução: {time.time() - start_time:.2f} segundos")