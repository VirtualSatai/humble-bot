import json

import requests
from bs4 import BeautifulSoup

FREE_ITEMS_URL = r"https://data1.origin.com/template/store/free-games/on-the-house.en-us.dnk.directive"
STORE_BASE = r"https://www.origin.com/dnk/en-us/store"
ALL_URL = r"https://api4.origin.com/supercat/DK/en_DK/supercat-PCWIN_MAC-DK-en_DK.json.gz"

def get_free_items():
    all_offers_res = requests.get(ALL_URL)
    if all_offers_res.status_code != 200:
        raise RuntimeError("Request returned error")

    all_offers = json.loads(all_offers_res.content)

    all_offers_res = requests.get(FREE_ITEMS_URL)
    if all_offers_res.status_code != 200:
        raise RuntimeError("Request returned error")

    soup = BeautifulSoup(all_offers_res.content, 'html.parser')
    on_the_house_items = soup.find_all(name="origin-store-oth-program")
    for item in on_the_house_items:
        game_path = item["ocd-path"]
        game_info = [b for b in all_offers['offers'] if b["offerPath"] == item['ocd-path']][0]
        print(f"dbg: {game_info['itemName']}: {STORE_BASE + game_path}")
        yield game_info

if __name__ == "__main__":
    for i in get_free_items():
        print(f"i['itemName']")
