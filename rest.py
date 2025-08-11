import requests
import time

token = "PERSONAL_TOKEN"

def get_popular_repositories(keyword):
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&page=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        print(f"Error: {response.status_code}")
        return []


def get_repository_details(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}")


def get_pull_requests(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed"
    headers = {"Authorization": f"Bearer {token}"}
    page = 1
    merged_count = 0
    while True:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            pull_requests = response.json()
            if not pull_requests:
                break
            for pr in pull_requests:
                # Buscar detalhes do PR para verificar se foi mesclado
                pr_url = pr["url"]
                pr_response = requests.get(pr_url, headers=headers)
                if pr_response.status_code == 200:
                    pr_details = pr_response.json()
                    if pr_details.get("merged_at"):
                        merged_count += 1
            page += 1
        else:
            raise Exception(f"Error: {response.status_code}")
    return merged_count

def get_releases(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Authorization": f"Bearer {token}"}
    page = 1
    releases = []
    while True:
        response = requests.get(f"{url}?page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_releases = response.json()
            if not page_releases:
                break
            releases.extend(page_releases)
            page += 1
        else:
            raise Exception(f"Error: {response.status_code}")
    return len(releases)

def get_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open"
    headers = {"Authorization": f"Bearer {token}"}
    page = 1
    issues = []
    while True:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_issues = response.json()
            if not page_issues:
                break
            issues.extend(page_issues)
            page += 1
        else:
            raise Exception(f"Error: {response.status_code}")
    return len(issues)

def get_clossed_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=closed"
    headers = {"Authorization": f"Bearer {token}"}
    page = 1
    closed_issues = []
    while True:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_closed_issues = response.json()
            if not page_closed_issues:
                break
            closed_issues.extend(page_closed_issues)
            page += 1
        else:
            raise Exception(f"Error: {response.status_code}")
    return len(closed_issues)

def get_repository_age(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repo_data = response.json()
        created_at = repo_data["created_at"]
        return created_at
    else:
        raise Exception(f"Error: {response.status_code}")

def get_last_updated(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repo_data = response.json()
        updated_at = repo_data["updated_at"]
        return updated_at
    else:
        raise Exception(f"Error: {response.status_code}")

def get_primary_language(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repo_data = response.json()
        primary_language = repo_data.get("language", "Unknown")
        return primary_language
    else:
        raise Exception(f"Error: {response.status_code}")

def collect_and_print_repo_data(repos):
    for repo in repos:
        owner = repo["owner"]["login"]
        repo_name = repo["name"]
        print(f"Repository: {owner}/{repo_name}")

        try:
            details = get_repository_details(owner, repo_name)
            print(f"Stars: {details['stargazers_count']}, Forks: {details['forks_count']}, Open Issues: {details['open_issues_count']}")

            pull_requests_count = get_pull_requests(owner, repo_name)
            print(f"Pull Requests: {pull_requests_count}")

            releases_count = get_releases(owner, repo_name)
            print(f"Releases: {releases_count}")

            closed_issues_count = get_clossed_issues(owner, repo_name)
            print(f"Closed Issues: {closed_issues_count}")

            open_issues_count = get_issues(owner, repo_name)
            print(f"Open Issues: {open_issues_count}")

            repo_age = get_repository_age(owner, repo_name)
            print(f"Repository Age: {repo_age}")

            last_updated = get_last_updated(owner, repo_name)
            print(f"Last Updated: {last_updated}")

            primary_language = get_primary_language(owner, repo_name)
            print(f"Primary Language: {primary_language}")

        except Exception as e:
            print(e)

        print("-" * 40)

def requisicao_automatica(intervalo_segundos=60):
    keyword = "open-source"
    while True:
        repos = get_popular_repositories(keyword)
        if repos:
            collect_and_print_repo_data(repos)
        else:
            print("Nenhum repositório encontrado.")
        time.sleep(intervalo_segundos)

if __name__ == "__main__":
    requisicao_automatica()