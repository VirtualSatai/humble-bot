import json

import zmq
from zmq import Context

TOPICFILTER = "0"

ctx = Context()

print("Connecting to the producer")
socket = ctx.socket(zmq.SUB)
socket.connect("tcp://humble-producer:5556")
socket.connect("tcp://origin-producer:5557")

socket.setsockopt_string(zmq.SUBSCRIBE, TOPICFILTER)

already_posted = set()


def filter_posted(items):
    global already_posted

    new_items = []
    for item in items:
        if item["name"] not in already_posted:
            already_posted.add(item["name"])
            new_items.append(item)

    return new_items


def process_items(items):
    global already_posted

    items = filter_posted(items)

    print(items)


while True:
    multipart = socket.recv_multipart()
    topic = multipart[0]
    messagedata = multipart[1]

    items = json.loads(messagedata)

    process_items(items)
