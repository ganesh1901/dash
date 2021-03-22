import zmq
import time
import sys


port = "5556"

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)


def GetServiceRequest():
    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: ", message)
        time.sleep(1)
        socket.send_string("World from %s" % port)


if __name__ == "__main__":
    GetServiceRequest()