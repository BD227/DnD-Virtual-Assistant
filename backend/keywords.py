import json
import os
import requests


KEYWORDS_FILE = "keywords.json"
BASE_URL = "https://api.open5e.com"

def fetch_keywords():
    """Fetch keywords (spells, items, and rules) from the Open5e API."""
    data = {"spells": [], "magicitems": []}

    for endpoint in ["spells", "magicitems"]:
        url = f"{BASE_URL}/{endpoint}/"
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                # Extract only the 'name' field for keywords
                items = [item.get('name') for item in result.get('results', [])]
                data[endpoint].extend(items)
                url = result.get('next')
            else:
                print(f"Failed to fetch {endpoint} data")
                return None

    return data

def save_keywords_to_file(keywords):
    """Save keywords to a local JSON file."""
    with open(KEYWORDS_FILE, "w") as f:
        json.dump(keywords, f)

def load_keywords_from_file():
    """Load keywords from a local JSON file."""
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r") as f:
            return json.load(f)
    return None

def get_keywords():
    """Fetch or load keywords when starting the server."""
    keywords = load_keywords_from_file()

    if not keywords:
        print("Keywords not found locally, fetching from Open5e API...")
        keywords = fetch_keywords()

        if keywords:
            save_keywords_to_file(keywords)
            return keywords
        else:
            print("Failed to fetch keywords from the Open5e API.")