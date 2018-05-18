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

print("Binding")
sender_socket = ctx.socket(zmq.PUB)
sender_socket.bind("tcp://*:5558")


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
    topic = b"1"

    items = filter_posted(items)
    for i in items:
        message = json.dumps(i).encode("utf-8")
        sender_socket.send_multipart([topic, message])
        print(f"Adding {i} to queue!")


while True:
    multipart = socket.recv_multipart()
    topic = multipart[0]
    messagedata = multipart[1]

    items = json.loads(messagedata)

    process_items(items)
