import json
import zmq
from zmq import Context

ctx = Context()

print("Connecting to the producer")
socket = ctx.socket(zmq.SUB)
socket.connect("tcp://humble-producer:5556")

topicfilter = "0"
socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

while True:
    multipart = socket.recv_multipart()
    topic = multipart[0]
    messagedata = multipart[1]
    free_stuff = json.loads(messagedata)
    print(topic, free_stuff)
