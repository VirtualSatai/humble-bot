import time
import json
import zmq

from zmq import Context

import requests

ctx = Context()

print("Binding to the socket")
socket = ctx.socket(zmq.PUB)
socket.bind("tcp://*:5556")

STORE_BASE_URL = r"https://www.humblebundle.com/store/"
JSON_URL = r"https://www.humblebundle.com/store/api/search?sort=discount&filter=onsale&request=1&page_size=20"  # noqa
TIMEOUT = 60


def get_free_items():
    res = requests.get(JSON_URL)

    if res.status_code != 200:
        raise RuntimeError("Request returned error")

    json_data = json.loads(res.content)
    free_items = [x for x in json_data['results']
                  if x['current_price'][0] == 0]

    for i in free_items:
        print(f"dbg: {i['human_name']}: {STORE_BASE_URL + i['human_url']}")

    items = [
        {
            "name": x["human_name"],
            "url": STORE_BASE_URL + x["human_url"],
            "price": x["current_price"],
        } for x in free_items
    ]

    return items


while True:
    topic = b"0"

    free_stuff = get_free_items()

    message = json.dumps(free_stuff).encode("utf-8")
    socket.send_multipart([topic, message])
    time.sleep(TIMEOUT)
