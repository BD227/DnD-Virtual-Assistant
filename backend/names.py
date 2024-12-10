import random
import requests

TAVERN_NAMES = [
        "The Sickly Parrots Inn",
        "The Molten Tauren Bar",
        "The Ethereal Leader Bar",
        "The Teeny Queen Tavern",
        "The Dry Ferret Tavern",
        "The Green Sheep Inn",
        "The Defiant Vampire",
        "The Old Fashioned Candle Tavern",
        "The Secret Pickaxe Bar",
        "The Fascinated Ferret Pub",
        "The Beautiful Sharks",
        "The Successful Loch Pub",
        "The Broken Angel Inn",
        "The Measly Lute Tavern",
        "The Giant Mango Pub",
        "The Lovely Demons",
        "The Naive Rats Bar",
        "The Second Jaguar",
        "The Yellow Mango",
        "The Red Elephant Seal",
        "The Future Well Inn",
        "The Organic Puppy Inn",
        "The Sudden Skies",
        "The Salty Gentlemen",
        "The Shouting Mandolin Bar",
        "The Abstract Carrot",
        "The Foolish Peanut Pub",
        "The Fluffy Elderberry",
        "The Teeny Guard Pub",
        "The Dapper Unicorns Pub",
        "The Dancing Clarinet",
        "The Deserted Nutmeg",
        "The Quacking Books",
        "The Grumpy Parsnip Tavern",
        "The Absent Desk Pub",
        "The Private Bongo",
        "The Laughable Helm Tavern",
        "The Dancing Flea Inn",
        "The Spectacular Peacock Bar",
        "The Triangular Rose",
        "The Jagged Sailboat Bar",
        "The Slow Trumpet Tavern",
        "The Snoring Snowfall Tavern",
        "The Ashamed Fly",
        "The Sleeping Whistle Bar",
        "The Harsh Beavers Pub",
        "The Attractive Eagle",
        "The Even Salad",
        "The Slippery Salad Tavern",
        "The Mature Meerkat Tavern",
        "The Rebel Vanilla",
        "The Nervous Dark Elf",
        "The Modern Loch Tavern",
        "The Frozen Truffle Tavern",
        "The Proud Crabs Bar",
        "The Mammoth Guard",
        "The Hissing Lamb Bar",
        "The Lazy Rats",
        "The Regular Lord",
        "Ye Olde Shipmate",
        "The Embarrassed Fork Pub",
        "The Slippery Cello",
        "The Drunken Unicorn",
        "The Dangerous Scream Inn",
        "The Incredible Ox Pub",
        "The Better Tavern",
        "The Frozen Salt Pub",
        "The Tame Fiddle",
        "The Moldy Gentlewoman",
        "The Magical Cup Tavern",
        "The Obedient Duduk Pub",
        "The Misty Husband Pub",
        "The Loving Nightingale",
        "The Jolly Meat",
        "The Threatening Melons Pub",
        "The Future Bamboo Pub",
        "The Short Loch Inn",
        "The Longing Badger",
        "The Demon Princess Bar",
        "The Fiery Belltower Bar",
        "The Jolly Corn Tavern",
        "The Round Hippopotamus Tavern",
        "The Panoramic Jester Pub",
        "The Green Lion Pub",
        "The Stormy Hazelnut",
        "The Victorious Dogs",
        "The Temporary Sign Bar",
        "The Wooden Sharks Bar",
        "The Vulgar Meerkat",
        "The Weak Fiddler Tavern",
        "The Aggressive Fork Bar",
        "The Lucky Horn Pub",
        "The Famous Nugget Tavern",
        "The Australian Fairy Bar",
        "The Thundering Bow",
        "The Fine Piano",
        "The Rotten Barricade Inn",
        "The Protective Bone Inn",
        "The Long Seahorse Inn",
        "The Skinny Angel",
        "The Different Shield",
        "The Nifty Apples Tavern",
        "The Tame Orangutan",
        "The Big Cod Tavern",
        "The Dapper Frog",
        "The False Nutmeg Inn",
        "The Polite Lady Bar",
        "The Teeny Cinnamon",
        "The Jaded Stag Inn",
        "The Laughing Elderberry",
        "The Wrong Wildebeest Inn",
        "The Jealous Shrub Tavern",
        "The Cold Rabbit",
        "The Triangular Cats Bar",
        "The Melting Discovery Pub",
        "The Fabulous Fish Inn",
        "The Dusty Goats Tavern",
        "The Sad Chimpanzee Tavern",
        "The Yellow Rabbit Pub",
        "The Armed Parrots",
        "The Mixed Knife",
        "The Freezing Sword Inn",
        "The Thin Caterpillar Bar",
        "The Lyrical Drum Tavern",
        "The Heavy Gentlewoman",
        "The Modern Sheep Bar",
        "The Spotless Narcissus Tavern",
        "The Stately Cloth Inn",
        "The Cheap Plate",
        "The Private Lyre",
        "The Worthless Turkey Inn",
        "The Diamond Chestplate",
        "The Gifted Hazelnut Bar",
        "The Quiet Snake",
        "The Shaggy Panda Inn",
        "The Wicked Crabs",
        "The Misty King Tavern",
        "The Colossal Demons Pub",
        "The Lucky Bee",
        "The Glistening Demons",
        "The Molten Oak",
        "The Armed Raccoon",
        "The Courageous Blossom Pub",
        "The Temporary Gooseberry",
        "The Flashy Crane",
        "The Dynamic Goats Pub",
        "The New Explorer Tavern",
        "The Broad Chestplate Tavern",
        "The Puzzled Fiddler Tavern",
        "The Keen Beavers",
        "The Rabid Steed",
        "The Quack Ape Pub",
        "The Royal Gang",
        "The Assorted Cabbage Bar",
        "The Jolly Night Tavern",
        "The Huge Books Bar",
        "The Loving Emu Inn",
        "The Mellow Bamboo Pub",
        "The Snobbish Eel",
        "The Far Parrots",
        "The Kind Cookie",
        "The Future Tower Bar",
        "The Discreet Banjo",
        "The Full Bats Pub",
        "The Dead Mice Bar",
        "The Kind Throne",
        "The Dynamic Elephant Seal",
        "The Next Peon Pub",
        "The Voiceless Flame Bar",
        "The Faint Cake Pub",
        "The Honorable Pickaxe Bar",
        "The Mysterious Horse",
        "The Eager Unicorns Pub"
    ]

RACE_KEYWORDS = {
    "dragonborn": ["draconian", "dragonlike"],
    "dwarf": ["dwarven"],
    "elf": ["elvin", "faerie", "fae"],
    "gnome": ["gnomish", "tinker"],
    "goblin": ["gob", "gobbo"],
    "halfling": ["hobbit", "halflingfolk"],
    "human": ["person", "humanfolk"],
    "orc": ["orcish", "greenskin", "ork"],
    "tiefling": ["infernal"],
    "troll": ["trollish", "trollfolk"],
}

TYPE_KEYWORDS = {
    "male": ["man"],
    "female": ["woman"],
    "family": [],
    "region": ["continent", "area", "zone"],
    "town": ["city", "village", "urban", "road", "market"],
    "tavern": ["bar", "pub", "inn", "alcohol", "drink", "beer", "ale", "food"]
}

NAME_COUNT = 12

def try_create_name_url(text):
    found_race = ""
    found_type = ""
    url = ""
    text = text.lower()
    for race, synonyms in RACE_KEYWORDS.items():
        if race in text:
            found_race = race
        if not found_race:
            for synonym in synonyms:
                if synonym in text:
                    found_race = race
    for type, synonyms in TYPE_KEYWORDS.items():
        if type in text:
            found_type = type
        if not found_type:
            for synonym in synonyms:
                if synonym in text:
                    found_type = type
    if found_race and not found_type:
        found_type = "female"
    if found_type and not found_race:
        found_race = "human"
    if found_race and found_type:
        url = f"https://names.ironarachne.com/race/{found_race}/{found_type}/{NAME_COUNT}"
    return url, found_race, found_type

def query_names(url):
    data = {}
    if "tavern" in url:
        names = random.sample(TAVERN_NAMES, NAME_COUNT)
        data = {'count': NAME_COUNT, 'names': names}
        return data
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"[Error querying names]: {e}")
        return {}
    
if __name__ == "__main__":
    text = "I want some ale"
    url = try_create_name_url(text)
    print(url)
    data = query_names(url)
    print(data)