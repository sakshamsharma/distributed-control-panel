#!/usr/bin/env python3

# Source: https://pymotw.com/3/socket/tcp.html

import json
import socket
import subprocess


def run(port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('0.0.0.0', port)
    sock.bind(server_address)
    print('Listening on {}:{}'.format(*server_address))

    # Listen for incoming connections
    sock.listen(1)

    try:
        while True:
            # Wait for a connection
            print('Waiting for a connection')
            connection, client_address = sock.accept()
            try:
                print('Connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16).decode("utf-8").strip()
                    print('Received {}'.format(data))
                    if data == 'die':
                        connection.sendall(b'Acknowledge kill signal')
                        raise ('Got kill signal')
                    else:
                        command = json.loads(data)
                        if command["action"] == "run":
                            ns = command["namespace"]
                            name = command["name"]
                            args = command["args"]
                            binary = command["binary"]
                            logs = command["logs"]
                            shell_cmd = "bash -c '{} {} > {}'".format(
                                binary, args, logs)
                            session_name = "{}-{}".format(ns, name),
                            ex = subprocess.call(["tmux", "new-session",
                                                  "-d", "-s",
                                                  session_name,
                                                  shell_cmd])
                            if ex != 0:
                                connection.sendall(
                                    b'{} command failed with exit code {}'
                                    .format(command["action"], ex))
                                continue
                        elif command["action"] == "kill":
                            ns = command["namespace"]
                            name = command["name"]
                            session_name = "{}-{}".format(ns, name),
                            ex = subprocess.call(["tmux", "kill-session",
                                                  "-t", session_name])
                            if ex != 0:
                                connection.sendall(
                                    b'{} command failed with exit code {}'
                                    .format(command["action"], ex))
                                continue
                        else:
                            connection.sendall(b'Unknown action {}'
                                               .format(command["action"]))
                            continue
                        connection.sendall(b'Acknowledge command')
                        # break
            finally:
                # Clean up the connection
                connection.close()
    finally:
        print('Shutting down')
        sock.close()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(port=7780)
