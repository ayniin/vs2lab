# Task worker
# Connects PULL socket to tcp://localhost:5557
# Collects workloads from ventilator via that socket
# Connects PUSH socket to tcp://localhost:5558
# Sends results to sink via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import sys
import time
import zmq
import constPipe
import threading

if len(sys.argv) != 2:
    print("Usage: mapper.py <number_worker>")
    sys.exit(1)

NUMBER_WORKER = int(sys.argv[1])


context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect(f"tcp://localhost:{constPipe.SPLITTER}")

# Socket to send messages to
reducer1 = context.socket(zmq.PUSH)
reducer1.connect(f"tcp://localhost:{constPipe.REDUCER1}")
reducer2 = context.socket(zmq.PUSH)
reducer2.connect(f"tcp://localhost:{constPipe.REDUCER2}")

def process(number):
    # Process tasks forever
    while True:
        s = receiver.recv()
        for word in s.decode().split(" "):
            if hash(word) % 2 == 0:
                print(f"Worker:{number} Sending word to reducer1: {word}")
                reducer1.send_string(word)
            else:
                print(f"Worker:{number} Sending word to reducer2: {word}")
                reducer2.send_string(word)
            
for i in range(NUMBER_WORKER):
    # Create a thread for each worker
    threading.Thread(target=process, args=(i,)).start()
