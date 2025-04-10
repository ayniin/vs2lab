"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True
    _telephone_book = {}  # empty telephone book

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))
        self._telephone_book = {
            "Hans": "1234",
            "Peter": "5678",
            "Paul": "91011",
            "Mary": "121314",
            "John": "151617",
            "Jane": "181920",
            "Björn": "212223"
        }

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped
                    data = data.decode('utf-8')  # decode data
                    self._logger.info("Received: " + data)
                    if data in "GETALL" and "GETALL" in data:
                        self._logger.info("GETALL")
                        # return all names
                        data = "\n".join([f"{name}: {number}" for name, number in self._telephone_book.items()])
                    elif data.startswith("GET"):
                        # GET request
                        if len(data.split()) != 2:
                            # wrong number of arguments
                            data = "Wrong number of arguments"
                        else:
                            name = data.split()[1]
                            if name in self._telephone_book:
                                # return telephone number
                                data = f"{self._telephone_book[name]}"
                            else:
                                # name not found
                                data = f"Name {name} not found"
                    else:
                        data = "Unknown command"
                    connection.send(data.encode('utf-8'))  # return sent data plus an "*"
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        """ Call server """
        self.sock.send(msg_in.encode('utf-8'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('utf-8')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def close(self):
        """ Close socket """
        self.sock.close()
