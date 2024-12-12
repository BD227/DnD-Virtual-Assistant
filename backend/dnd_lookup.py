import uuid
import requests

def query_open5e(category, keyword):
    """
    Query the Open5e API for the given category and keyword.
    """
    url = keyword['url']
    if not url:
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
        "magicitems": "Magic Item",
        "monsters": "Monster",
        "planes": "Plane",
        "feats": "Feat",
        "conditions": "Condition",
        "races": "Race",
        "classes": "Class",
        "weapons": "Weapon",
        "armor": "Armor"
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
        "requires_attunement": data.get("requires_attunement"),
        # Monsters
        "size": data.get("size"),
        "armor_class": data.get("armor_class"),
        "strength": data.get("strength"),
        "strength": data.get("strength"),
        "dexterity": data.get("dexterity"),
        "constitution": data.get("constitution"),
        "intelligence": data.get("intelligence"),
        "wisdom": data.get("wisdom"),
        "charisma": data.get("charisma"),
        "strength_save": data.get("strength_save"),
        "dexterity_save": data.get("dexterity_save"),
        "constitution_save": data.get("constitution_save"),
        "intelligence_save": data.get("intelligence_save"),
        "wisdom_save": data.get("wisdom_save"),
        "charisma_save": data.get("charisma_save"),
        # Feats
        "benefits": data.get("benefits"),
        # Races
        "traits": data.get("traits"),
        # Weapons
        "is_versatile": data.get("is_versatile"),
        "is_martial": data.get("is_martial"),
        "is_melee": data.get("is_melee"),
        "ranged_attack_possible": data.get("ranged_attack_possible"),
        "range_melee": data.get("range_melee"),
        "is_reach": data.get("is_reach"),
        "properties": data.get("properties"),
        "distance_unit": data.get("distance_unit"),
        "name": data.get("name"),
        "damage_dice": data.get("damage_dice"),
        "versatile_dice": data.get("versatile_dice"),
        "reach": data.get("reach"),
        "range": data.get("range"),
        "long_range": data.get("long_range"),
        "is_finesse": data.get("is_finesse"),
        "is_thrown": data.get("is_thrown"),
        "is_two_handed": data.get("is_two_handed"),
        "requires_ammunition": data.get("requires_ammunition"),
        "requires_loading": data.get("requires_loading"),
        "is_heavy": data.get("is_heavy"),
        "is_light": data.get("is_light"),
        "is_lance": data.get("is_lance"),
        "is_net": data.get("is_net"),
        "is_simple": data.get("is_simple"),
        "is_improvised": data.get("is_improvised"),
        # Armor
        "ac_display": data.get("ac_display"),
        "ac_base": data.get("ac_base"),
        "grants_stealth_disadvantage": data.get("grants_stealth_disadvantage"),
        "strength_score_required": data.get("strength_score_required"),
    }



if __name__ == "__main__":
    found_keywords = {"spells": [{"name": "Fireball", "slug": "fireball"}], 'monsters': [{"name": "Adult Amethyst Dragon", "slug": "adult-amethyst-dragon-a5e"}], "magicitems": [{"name": "Amulet of Health", "slug": "amulet-of-health-a5e"}]}
    query_results = query_open5e_for_keywords(found_keywords)
    for item in query_results:
        print(f"\nCategory: {item['category']}")
        print(f"- {item['name']}: {item.get('desc', 'No description available.')}")