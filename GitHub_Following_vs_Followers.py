# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import requests

def get_all_pages(url, headers):
    results = []
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        results.extend(data)
        page += 1
    return results

def get_github_data(username, headers):
    followers_url = f"https://api.github.com/users/{username}/followers"
    following_url = f"https://api.github.com/users/{username}/following"
    
    followers = [follower['login'] for follower in get_all_pages(followers_url, headers)]
    following = [user['login'] for user in get_all_pages(following_url, headers)]
    
    return followers, following

def find_non_followers(followers, following):
    non_followers = set(following) - set(followers)
    return non_followers

def unfollow_users(username, users, headers):
    exceptions = {"ExceptionPersonHere"}
    for user in users:
        if user not in exceptions:
            unfollow_url = f"https://api.github.com/user/following/{user}"
            response = requests.delete(unfollow_url, headers=headers)
            if response.status_code == 204:
                print(f"Successfully unfollowed {user}")
            else:
                print(f"Failed to unfollow {user}")

def follow_users(username, users, headers):
    exceptions = {"insertexceptionpersonhere"}
    for user in users:
        if user not in exceptions:
            follow_url = f"https://api.github.com/user/following/{user}"
            response = requests.put(follow_url, headers=headers)
            if response.status_code == 204:
                print(f"Successfully followed {user}")
            else:
                print(f"Failed to follow {user}")

def main():
    username = input("Please enter your GitHub username: ").strip()
    token = input("Please enter your GitHub personal access token: ").strip()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    followers, following = get_github_data(username, headers)

    to_follow = set(followers) - set(following)
    print("Users to follow:", to_follow)

    follow_users(username, to_follow, headers)

    non_followers = find_non_followers(followers, following)
    print("Users followed but not following back:", non_followers)

    unfollow_users(username, non_followers, headers)

if __name__ == "__main__":
    main()
