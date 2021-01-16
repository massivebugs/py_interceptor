#!/usr/bin/python3
from socket import *
import ssl
from proxxy_http import HTTPRequest
from httptools import HttpRequestParser, HttpParserUpgrade
import sys, os

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(os.getcwd() + '/certificate.pem', os.getcwd() + '/privkey.pem')

with socket(AF_INET, SOCK_STREAM) as new_server_sock:
    # Create welcoming socket
    new_server_sock.bind(('127.0.0.1', 8443))

    # maximum of 10 queues
    new_server_sock.listen()
    with context.wrap_socket(new_server_sock, server_side=True) as tls_proxxy_sock:
        while True:
            tls_proxxy_client_sock, addr = tls_proxxy_sock.accept()
            #while data := tls_proxxy_client_sock.recv(1024):
            #    print(data)

            http_request = HTTPRequest()
            parser = HttpRequestParser(http_request)
            # keep receiving until end of message
            while not http_request.complete:
                try:
                    parser.feed_data(tls_proxxy_client_sock.recv(2048))
                except HttpParserUpgrade:
                    pass

            # Finish constructing the message in the http_request
            http_request.method = parser.get_method()
            http_request.version = parser.get_http_version()

            print(http_request.collect_message())
            tls_proxxy_client_sock.close()

