import json
import time

import requests
import zmq
from bs4 import BeautifulSoup
from zmq import Context

FREE_ITEMS_URL = r"https://data1.origin.com/template/store/free-games/on-the-house.en-us.dnk.directive"
STORE_BASE_URL = r"https://www.origin.com/dnk/en-us/store"
ALL_URL = r"https://api4.origin.com/supercat/DK/en_DK/supercat-PCWIN_MAC-DK-en_DK.json.gz"
TIMEOUT = 60

ctx = Context()
print("Binding")
socket = ctx.socket(zmq.PUB)
socket.bind("tcp://*:5557")


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
        print(f"dbg: {game_info['itemName']}: {STORE_BASE_URL + game_path}")
        item = {
            "name": game_info["itemName"],
            "url": STORE_BASE_URL + game_path,
            "price": [0.0, "EUR"],
        }
        yield item

# Wait for system to start
time.sleep(5)

while True:
    topic = b"0"
    free_stuff = list(get_free_items())

    message = json.dumps(free_stuff).encode("utf-8")
    socket.send_multipart([topic, message])
    time.sleep(TIMEOUT)
