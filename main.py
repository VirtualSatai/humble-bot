import json
import os
from time import sleep

import requests
from slackclient import SlackClient

SLACK_CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
STORE_BASE_URL = r'https://www.humblebundle.com/store/'
JSON_URL = r"https://www.humblebundle.com/store/api/search?sort=discount&filter=onsale&request=1&page_size=20"
TIMEOUT = 60

def get_free_items():
    res = requests.get(JSON_URL)

    if res.status_code != 200:
        raise RuntimeError("Request returned error")

    json_data = json.loads(res.content)
    free_items = [x for x in json_data['results'] if x['current_price'][0] <= 1]

    return free_items

if __name__ == "__main__":
    sc = SlackClient(SLACK_BOT_TOKEN)
    already_posted = list()

    while True:
        free_stuff = get_free_items()
        to_post = [i for i in free_stuff if i['human_name'] not in [j['human_name'] for j in already_posted]]
        for p in to_post:
            message = f"{p['human_name']} is free at {STORE_BASE_URL + p['human_url']}"
            print(f"Posting: {message}")
            sc.api_call(
                "chat.postMessage",
                channel=SLACK_CHANNEL_ID,
                text=message,
            )
            already_posted.append(p)
        if len(to_post) == 0:
            print("Didn't post any thing")

        sleep(TIMEOUT)
