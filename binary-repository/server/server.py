#!/usr/bin/env python3

import http.server
import socketserver
import os

PORT = 8001

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_PUT(self):
        path = "." + self.path
        if os.path.exists(path) and ("If-None-Match" in self.headers):
            self.send_response(412)
            self.end_headers()
            return

        os.makedirs(os.path.dirname(path), exist_ok=True)
        length = int(self.headers['Content-Length'])
        with open(path, "wb") as f:
            f.write(self.rfile.read(length))
        self.send_response(200)
        self.end_headers()


httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
