import uuid
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

    print(f"Query Complete.")
    return results

def trimData(data, category):
    category_mapping = {
        "spells": "Spell",
        "magicitems": "Magic Item"
    }
    return {
        "id": str(uuid.uuid4()),
        "category": category_mapping[category],
        "name": data.get("name"),
        "desc": data.get("desc"),
        # Spells
        "higher_level": data.get("higher_level"),
        "range": data.get("range"),
        "duration": data.get("duration"),
        "requires_concentration": data.get("requires_concentration"),
        "casting_time": data.get("casting_time"),
        "level": data.get("level"),
        # Magic Items
        "type": data.get("type"),
        "rarity": data.get("rarity"),
        "requires_attunement": data.get("requires_attunement")
    }



if __name__ == "__main__":
    found_keywords = {"spells": [{"name": "Fireball", "slug": "fireball"}], 'monsters': [{"name": "Adult Amethyst Dragon", "slug": "adult-amethyst-dragon-a5e"}], "magicitems": [{"name": "Amulet of Health", "slug": "amulet-of-health-a5e"}]}
    query_results = query_open5e_for_keywords(found_keywords)
    for item in query_results:
        print(f"\nCategory: {item['category']}")
        print(f"- {item['name']}: {item.get('desc', 'No description available.')}")