import json
import os
import time

import zmq

from slackclient import SlackClient
from zmq import Context

SLACK_CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
TOPICFILTER = "1"
TIMEOUT = 1

ctx = Context()

print("Connecting to the producer")
socket = ctx.socket(zmq.SUB)
socket.connect("tcp://product-consumer:5558")

socket.setsockopt_string(zmq.SUBSCRIBE, TOPICFILTER)

sc = SlackClient(SLACK_BOT_TOKEN)

while True:
    multipart = socket.recv_multipart()
    topic = multipart[0]
    data = multipart[1]
    item = json.loads(data)
    message = f"{item['name']} costs {item['price'][0]} {item['price'][1]} at {item['url']}"
    print(f"Posting: {message}")
    sc.api_call(
        "chat.postMessage",
        channel=SLACK_CHANNEL_ID,
        text=message,
    )
    time.sleep(TIMEOUT)
