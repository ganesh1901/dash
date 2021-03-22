import zmq
import sys
import json


port = "5556"
context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
#  Do 10 requests, waiting each time for a response
# for request in range (1,10):
request = 0
while True:
    request += 1
    print("Sending request ", request,"...")
    socket.send_string("Hello")
    #  Get the reply.
    message = socket.recv()
    print("Received reply ", request, "[", message, "]")
