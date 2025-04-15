# Task ventilator
# Binds PUSH socket to tcp://localhost:5557
# Sends batch of tasks to workers via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import zmq
import random
import time
import constPipe

context = zmq.Context()

# Socket to send messages on
sender = context.socket(zmq.PUSH)
sender.bind(f"tcp://*:{constPipe.SPLITTER}")

file = open("workload.txt", "r")
workload = file.readlines()
file.close()

for line in workload:
    print(f"Sending {line}")
    sender.send_string(f"{line}")

