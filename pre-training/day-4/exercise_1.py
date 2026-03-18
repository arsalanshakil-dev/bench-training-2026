import sys
import requests

BASE_URL = "https://api.github.com"


def fetch_user_profile(username):
    try:
        response = requests.get(f"{BASE_URL}/users/{username}")

        if response.status_code == 404:
            print(f"Error: User '{username}' not found.")
            return None
        elif response.status_code == 403:
            print("Error: Rate limit exceeded. Try again later.")
            return None
        elif response.status_code != 200:
            print(f"Error: Unexpected status code {response.status_code}")
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"🌐 Network Error: {e}")
        return None


def fetch_repositories(username):
    try:
        repos = []
        page = 1

        while True:
            response = requests.get(
                f"{BASE_URL}/users/{username}/repos",
                params={"per_page": 100, "page": page}
            )

            if response.status_code != 200:
                print("Error fetching repositories.")
                return []

            data = response.json()
            if not data:
                break

            repos.extend(data)
            page += 1

        return repos

    except requests.exceptions.RequestException as e:
        print(f"🌐 Network Error while fetching repos: {e}")
        return []


def display_user_info(user, repos):
    print("\n===== GitHub User Profile =====")
    print(f"Username       : {user.get('login')}")
    print(f"Bio            : {user.get('bio')}")
    print(f"Public Repos   : {user.get('public_repos')}")
    print(f"Followers      : {user.get('followers')}")

    # Sort repos by stars
    top_repos = sorted(
        repos,
        key=lambda x: x.get("stargazers_count", 0),
        reverse=True
    )[:5]

    print("\n===== Top 5 Repositories by Stars =====")
    if not top_repos:
        print("No repositories found.")
        return

    for repo in top_repos:
        print(
            f"- {repo.get('name')} | ⭐ {repo.get('stargazers_count')} | "
            f"Language: {repo.get('language')}"
        )


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <github_username>")
        return

    username = sys.argv[1]

    user = fetch_user_profile(username)
    if not user:
        return

    repos = fetch_repositories(username)
    display_user_info(user, repos)


if __name__ == "__main__":
    main()