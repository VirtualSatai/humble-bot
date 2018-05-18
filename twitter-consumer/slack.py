import json
import os
import time

import zmq

import twitter
from zmq import Context

api = twitter.Api(
    consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
    consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
    access_token_key=os.environ["TWITTER_ACCESS_KEY"],
    access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
)
ctx = Context()

TOPICFILTER = "1"

print("Connecting to the producer")
socket = ctx.socket(zmq.SUB)
socket.connect("tcp://product-consumer:5558")

socket.setsockopt_string(zmq.SUBSCRIBE, TOPICFILTER)

while True:
    multipart = socket.recv_multipart()
    topic = multipart[0]
    data = multipart[1]
    item = json.loads(data)
    message = f"{item['name']} costs {item['price'][0]} {item['price'][1]} at {item['url']}"
    print(f"Posting: {message}")
    api.PostUpdate(message)
