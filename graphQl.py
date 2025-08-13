import requests
import time
import keyring
import os

service_name = "GITHUB_API_TOKEN"
username = "LAB_EXPERIMENTACAO"

# Tenta obter o token do gerenciador de senhas do sistema (Keychain, Windows Credential Manager, etc.)
TOKEN = keyring.get_password(service_name, username)

# Se o token não for encontrado no gerenciador de senhas, tenta ler de uma variável de ambiente
if not TOKEN:
    print("Token não encontrado no keyring. Tentando ler da variável de ambiente 'GITHUB_API_TOKEN'...")
    TOKEN = os.getenv("GITHUB_API_TOKEN")

# Se o token ainda não for encontrado, o código deve levantar um erro
if not TOKEN:
    raise ValueError("Token de autenticação não encontrado. Por favor, defina-o no keyring ou na variável de ambiente 'GITHUB_API_TOKEN'.")

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

def get_top_repo_ids(total_repos=100):
    repos = []
    cursor = None
    per_page = 100

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

def collect_and_print_repo_data():
    repos = get_top_repo_ids(100)
    for repo in repos:
        details = get_repo_details(repo["owner"]["login"], repo["name"])
        primary_language = details['primaryLanguage']['name'] if details['primaryLanguage'] else 'Unknown'
        open_issues = details['issues']['totalCount']
        closed_issues = details['closedIssues']['totalCount']
        total_issues = open_issues + closed_issues
        closed_ratio = (closed_issues / total_issues) if total_issues > 0 else 0

        print(f"Repository: {repo['owner']['login']}/{repo['name']}")
        print(f"Stars: {details['stargazerCount']}")
        print(f"Repository Age: {details['createdAt']}")
        print(f"Last Updated: {details['updatedAt']}")
        print(f"Primary Language: {primary_language}")
        print(f"Releases: {details['releases']['totalCount']}")
        print(f"Open Issues: {open_issues}")
        print(f"Closed Issues: {closed_issues}")
        print(f"Closed Issues Ratio: {closed_ratio:.2f}")
        print(f"Merged Pull Requests: {details['pullRequests']['totalCount']}")
        print("-" * 40)

if __name__ == "__main__":
    start_time = time.time()
    collect_and_print_repo_data()
    print(f"Tempo total de execução: {time.time() - start_time:.2f} segundos")