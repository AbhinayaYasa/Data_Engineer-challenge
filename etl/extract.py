import requests
import logging

def fetch_data(endpoint):
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        logging.info(f"Fetched data from {endpoint}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {endpoint}: {e}")
        return []

USERS_API = "https://jsonplaceholder.typicode.com/users"
POSTS_API = "https://jsonplaceholder.typicode.com/posts"
