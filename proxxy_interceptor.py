#!/usr/bin/python3
from socket import *
import ssl
from proxxy_args import parse_args
from proxxy_http import HTTPRequest
from httptools import HttpRequestParser, HttpParserUpgrade
import sys, os

args = parse_args()

with socket(AF_INET, SOCK_STREAM) as proxy_sock:
    # Create welcoming socket
    proxy_sock.bind((args.address, args.port))

    # maximum of 10 queues
    proxy_sock.listen()
    print(f'Intercepting requests at "{args.address}:{args.port}"\n')

    # Synchronously listen to requests
    while True:
        client_sock, addr = proxy_sock.accept()

        http_request = HTTPRequest()
        parser = HttpRequestParser(http_request)
        # keep receiving until end of message
        while not http_request.complete:
            try:
                parser.feed_data(client_sock.recv(2048))
            except HttpParserUpgrade:
                pass

        # Finish constructing the message in the http_request
        http_request.method = parser.get_method()
        http_request.version = parser.get_http_version()

        # SSL Tunneling
        if http_request.method == 'CONNECT':
            # Upgrade socket to tls socket on separate process
            try:
                destination_sock = socket(AF_INET, SOCK_STREAM)
                destination_sock.connect(('127.0.0.1', 8443))
            except:
                print('dest sock error')

            # Return OK to client_sock
            client_sock.sendall('HTTP/1.1 200 OK\r\n\r\n'.encode())
            client_sock.setblocking(0)
            destination_sock.setblocking(0)
            print('Forwarding everything')
            while True:
                try:
                    cr =  client_sock.recv(1024) 
                    destination_sock.sendall(cr)
                except Exception as e:
                    pass
                try:
                    dr = destination_sock.recv(1024)
                    client_sock.sendall(dr)
                except Exception as e:
                    pass

        # No SSL Tunneling
        else:
            print(http_request.collect_message())
            client_sock.sendall('HTTP/1.1 200 OK\r\n\r\n'.encode())

        client_sock.close()
        break

    print("Exiting proxxy...")
