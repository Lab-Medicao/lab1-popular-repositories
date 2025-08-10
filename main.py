import requests

token = "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"

def get_popular_repositories(keyword, num_repos):
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&page={num_repos}"
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
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all"
    headers = {"Authorization": f"Bearer {token}"}
    page = 1
    pull_requests = []
    while True:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_pull_requests = response.json()
            if not page_pull_requests:
                break
            pull_requests.extend(page_pull_requests)
            page += 1
        else:
            raise Exception(f"Error: {response.status_code}")
    return len(pull_requests)

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

        except Exception as e:
            print(e)

        print("-" * 40)


if __name__ == "__main__":
    keyword = "machine learning"
    num_repos = 10  # Change this to get more pages of results
    repos = get_popular_repositories(keyword, num_repos)

    if repos:
        collect_and_print_repo_data(repos)
    else:
        print("No repositories found.")