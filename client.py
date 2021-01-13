# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:16:56 2021

@author: Rastko
"""

import socket
from socket import SOCK_DGRAM


class client:
    """The client side for commmunicating with sockets

    Parameters
    ----------
    HOST : str:`192.168.0.51`, optional
        The IP address of the server that the client will connect to
    PORT : int:9077, optional
        The port that the server is accessible by.


    Attributes
    ----------
    s : socket
        The socket object which is used to communicate to the server
    HOST : str:`192.168.0.51`
        The IP address of the server that the client will connect to
    PORT : int:9077
        The port that the server is accessible by.

    """

    def __init__(self, HOST="192.168.0.51", PORT=9077):
        """Initialises the client class."""
        self.s = socket.socket(type=SOCK_DGRAM)
        self.HOST = HOST
        self.PORT = PORT

    def send_message(self, message):
        """Sends a message to the server that the socket is connected to

        message : str
            A string of text to send to the server
        """
        self.s.sendto(str(message).encode(), (self.HOST, self.PORT))
        return None

