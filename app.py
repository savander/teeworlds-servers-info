#!/usr/bin/env python3

import os
import json
import argparse
import tw_api

def save_to_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(data)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Teeworlds Servers Info tool to extract details about servers to JSON.',
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='TW Servers Info v0.1.0',
    )

    parser.add_argument(
        '-f', '--file',
        dest='file',
        default='servers.json',
        help='the name of the file that will store servers info',
    )

    parser.add_argument(
        '-p', '--path',
        dest='path',
        default=os.getcwd(),
        help='the store path of the servers info file '
             '(`servers.json` by default, can be set via `-f` or `--file` argument)',
    )

    parser.add_argument(
        '-t', '--timeout',
        dest='timeout',
        default=2,
        type=float,
        help='set a timeout after which script will stop trying to listen for data from the server',
    )

    parser.add_argument(
        '-s', '--server',
        dest='servers',
        action="append",
        required=True,
        nargs=2,
        metavar=('NAME', 'ADDRESS'),
        help='the server name and address with port e.g. `--server "Server01" "127.0.0.1:8303"` '
             'can be used multiple times, to add multiple servers.',
    )

    return parser.parse_args()


def get_servers_info(servers):
    parsed_servers = {}

    for server in servers:
        name = str(server[0])
        parsed_address = server[1].split(':')

        address = str(parsed_address[0])
        port = int(parsed_address[1]) if len(parsed_address) > 1 else 8303

        parsed_servers[name] = tw_api.get_server_info((address, port))

    return parsed_servers


def execute():
    arguments = parse_arguments()

    tw_api.TIMEOUT = arguments.timeout

    path = os.path.join(
        arguments.path,
        arguments.file
    )

    servers = get_servers_info(arguments.servers)

    servers_json = json.dumps(servers, indent=2)

    save_to_file(path, servers_json)


if __name__ == '__main__':
    execute()
