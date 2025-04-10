import rpc
import logging
import time
import threading

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

# Event zum Signalisieren, dass der Callback abgeschlossen ist
result_ready = threading.Event()
result_value = None

# Callback-Funktion
def result_callback(result, error=None):
    global result_value
    if error:
        print(f"Error: {error}")
    else:
        result_value = result
        print(f"Callback received result: {result}")
    result_ready.set()  # Signal, dass der Callback ausgeführt wurde

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, callback=result_callback)

# Warten und zählen (wie vorher)
for i in range(1, 15):
    print(i)
    time.sleep(1)

cl.stop()