#!/usr/bin/env python3
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Written by Nathan Hamiel (2010)

from http.server import HTTPServer, BaseHTTPRequestHandler
import pickle
import actions
import subprocess


should_run = True
dummy = actions.RunAction("", "", "", "", "")
list_of_tmux_sessions_running = []


def keep_running():
    return should_run


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global should_run

        request_path = self.path

        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)
        print("Request headers:", self.headers)
        print("<----- Request End -----\n")

        if request_path == '/die':
            should_run = False
            for sess in list_of_tmux_sessions_running:
                subprocess.call(["tmux", "kill-session", "-t", sess])

        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()

    def do_POST(self):
        global list_of_tmux_sessions_running

        request_path = self.path

        print("\n----- Request Start ----->\n")
        print("Request path:", request_path)

        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0
        data = self.rfile.read(length)

        print("Content Length:", length)
        print("Request headers:", request_headers)
        print("Request payload:", data)
        print("<----- Request End -----\n")

        if request_path == '/run':
            x = pickle.loads(data)
            print(x.shell_cmd)
            ex = subprocess.call(["tmux", "new-session",
                                  "-d", "-s",
                                  x.session_name, x.shell_cmd])
            if ex != 0:
                self.send_response(500)
                self.end_headers()
                return
            list_of_tmux_sessions_running.append(x.session_name)
        elif request_path == '/stop':
            x = pickle.loads(data)
            print(x.session_name)
            ex = subprocess.call(["tmux", "kill-session",
                                  "-t", x.session_name])
            if ex != 0:
                self.send_response(500)
                self.end_headers()
                return
            list_of_tmux_sessions_running.remove(x.session_name)

        self.send_response(200)
        self.end_headers()

    do_PUT = do_POST
    do_DELETE = do_GET


def run(port):
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print('Listening on {}:{}'.format('0.0.0.0', port))
    while keep_running():
        server.handle_request()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(port=7780)
