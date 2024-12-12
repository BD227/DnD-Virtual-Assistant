from collections import defaultdict
import json
import os
import string
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
import requests


KEYWORDS_FILE = "keywords.json"
BASE_URL = "https://api.open5e.com"

def get_endpoints():
    endpoints = {"spells": "", "magicitems": "", "monsters": "", "planes": "", "feats": "", "conditions": "", "races": "", "classes": "", "weapons": "", "armor": ""}
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        result = response.json()
        for category in result:
            if category in endpoints.keys():
                endpoints[category] = result[category]
    return endpoints


def fetch_keywords(endpoints):
    """Fetch keywords (spells, items, and rules) from the Open5e API."""
    data = {"spells": [], "magicitems": [], "monsters": [], "planes": [], "feats": [], "conditions": [], "races": [], "classes": [], "weapons": [], "armor": []}

    for category, url in endpoints.items():
        print(f"Fetching {category} from {url}...")
        while url:
            response = requests.get(url)
            if response.status_code == 200:
                print("Response received!")
                result = response.json()
                # Extract 'name' and 'slug' fields for lookup
                items = [
                    {
                        "name": item.get('name'),
                        "url": item.get('url'),
                        "slug": item.get('slug')
                    }
                    for item in result.get('results', [])
                    if item.get('name')
                    and (item.get('url') or item.get('slug'))
                    and ('a5e' not in (item.get('url') or "") and 'a5e' not in (item.get('slug') or ""))
                ]

                for item in items:
                    print(item.get("name") + " added")

                data[category].extend(items)
                url = result.get('next')
            else:
                print(f"Failed to fetch {category} data")
                url = increment_page_number(url)
                response = requests.get(url)
                if response.status_code == 200:
                    print("Response received!")
                    result = response.json()
                    # Extract 'name' and 'slug' fields for lookup
                    items = [
                        {
                            "name": item.get('name'),
                            "url": item.get('url'),
                            "slug": item.get('slug')
                        }
                        for item in result.get('results', [])
                        if item.get('name')
                        and (item.get('url') or item.get('slug'))
                        and ('a5e' not in (item.get('url') or "") and 'a5e' not in (item.get('slug') or ""))
                    ]


                    data[category].extend(items)
                    url = result.get('next')
                else:
                    print(f"Failed to fetch {category} data")
                    url = ""


    return data

def increment_page_number(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Extract query parameters as a dictionary
    query_params = parse_qs(parsed_url.query)
    
    # Increment the page number if it exists
    if 'page' in query_params:
        query_params['page'] = [str(int(query_params['page'][0]) + 1)]
    
    # Construct the updated query string
    updated_query = urlencode(query_params, doseq=True)
    
    # Reconstruct the URL with the updated query
    new_url = urlunparse(parsed_url._replace(query=updated_query))
    return new_url

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
    endpoints = get_endpoints()
    keywords = fetch_keywords(endpoints)
    print("Keywords Fetched!")

    if keywords:
        save_keywords_to_file(keywords)
    else:
        print("Failed to fetch keywords from the Open5e API.")
    return keywords
    

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

if __name__ == "__main__":
    get_keywords()
    print(f"Fetching Complete")
