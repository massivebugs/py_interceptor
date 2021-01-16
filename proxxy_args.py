import argparse

def parse_args():
    # Parse arguments
    parser = argparse.ArgumentParser(
            description = 'Proxy server for manipulating payloads flexibly',
            epilog = 'written by massivebugs')

    # ip address
    parser.add_argument('-a', '--address', default='127.0.0.1', type=str, help='ip address of the proxy server')
    # port designation
    parser.add_argument('-p', '--port', default=8080, type=int, help='port number of the proxy server')
    # caching usage
    parser.add_argument('-c', '--cache', action='store_true', help='use caching feature')

    return parser.parse_args()

