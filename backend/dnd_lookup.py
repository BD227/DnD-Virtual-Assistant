import requests

def query_open5e(category, keyword):
    """
    Query the Open5e API for the given category and keyword.
    """
    base_url = "https://api.open5e.com/"

    slug = keyword['slug']

    url = f"{base_url}{category}/{slug}"
    print(f"Querying {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"[Error querying Open5e]: {e}")
        return []

def query_open5e_for_keywords(found_keywords):
    """
    Query the Open5e API for all matched keywords in their respective categories.
    """
    results = []

    for category, keywords in found_keywords.items():
        for keyword in keywords:
            data = query_open5e(category, keyword)
            if data:
                data = trimData(data,category)
                results.append(data)

    print(f"Query Complete: {results}")
    return results

def trimData(data, category):
    return {
        "category": category,
        "name": data['name'],
        "desc": data['desc'],
    }


if __name__ == "__main__":
    found_keywords = {"spells": [{"name": "Fireball", "slug": "fireball"}], 'monsters': [{"name": "Adult Amethyst Dragon", "slug": "adult-amethyst-dragon-a5e"}], "magicitems": [{"name": "Amulet of Health", "slug": "amulet-of-health-a5e"}]}
    query_results = query_open5e_for_keywords(found_keywords)
    for item in query_results:
        print(f"\nCategory: {item['category']}")
        print(f"- {item['name']}: {item.get('desc', 'No description available.')}")