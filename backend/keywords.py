from collections import defaultdict
import json
import os
import string
import requests


KEYWORDS_FILE = "keywords.json"
BASE_URL = "https://api.open5e.com"

def fetch_keywords():
    """Fetch keywords (spells, items, and rules) from the Open5e API."""
    data = {"spells": [], "magicitems": []}

    for endpoint in ["spells", "magicitems"]:
        print(f"Fetching {endpoint}...")
        url = f"{BASE_URL}/{endpoint}/"
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                print("Response received!")
                result = response.json()
                # Extract 'name' and 'slug' fields for lookup
                items = [
                    {
                        "name": item.get('name'),
                        "slug": item.get('slug')
                    }
                    for item in result.get('results', [])
                    if 'name' in item and 'slug' in item and 'a5e' not in item.get('slug')
                ]

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

    if keywords:
        print("Keywords found locally")
        return keywords

    print("Keywords not found locally, fetching from Open5e API...")
    keywords = fetch_keywords()
    print("Keywords Fetched!")
    #keywords = deduplicate_keywords(keywords)
    #print("Deduplication complete!")

    if keywords:
        save_keywords_to_file(keywords)
    else:
        print("Failed to fetch keywords from the Open5e API.")
    return keywords

def deduplicate_keywords(keywords):
    """
    Deduplicate keywords in each category of the dictionary.
    """
    seen = set()
    deduplicated = {}
    for category, keyword_list in keywords.items():
        deduplicated[category] = []
        for item in keyword_list:
            identifier = item.get("name")
            if identifier not in seen:
                seen.add(identifier)
                deduplicated[category].append(item)
    return deduplicated
    

def find_keywords(text):
    """
    Finds keywords in the given text using fuzzy matching.
    Only matches if the similarity score is greater than the threshold.
    """
    if not text:
        return defaultdict(list)

    keywords = get_keywords()
    if not keywords:
        raise ValueError("Keywords cannot be None or empty.")

    found_keywords = defaultdict(list)
    print("Processing text")
    text = preprocess_text(text)

    for category, keyword_list in keywords.items():
        for keyword in keyword_list:
            name = preprocess_text(keyword['name'])
            if name in text:
                found_keywords[category].append(keyword)
    
    # Deduplicate results in the found_keywords dictionary
    #print("Deduplicating keywords")
    #deduplicate_keywords(found_keywords)

    # Deduplicate the found keywords
    return found_keywords

def preprocess_text(text):
    """
    Strip spaces and punctuation from a string and convert to lowercase.
    """
    return ''.join(char for char in text if char not in string.punctuation).replace(" ", "").lower()
