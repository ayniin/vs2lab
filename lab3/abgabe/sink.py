import sys
import time
import zmq
import constPipe

context = zmq.Context()

# Socket to receive messages on
if len(sys.argv) != 2:
    print("Usage: sink.py <port>")
    sys.exit(1)
receiver = context.socket(zmq.PULL)
if sys.argv[1] == "1":
    receiver.bind(f"tcp://*:{constPipe.REDUCER1}")
elif sys.argv[1] == "2":
    receiver.bind(f"tcp://*:{constPipe.REDUCER2}")
else:
    print("Invalid argument. Use 1 or 2.")
    sys.exit(1)

word_count = {}
while True:
    s = receiver.recv()
    word = s.decode()
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

    print(f"Received word: {word}, count: {word_count[word]}")