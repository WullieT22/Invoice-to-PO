#!/usr/bin/env python3
"""Simple HTTP server to serve app.html"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 8080
DIRECTORY = str(Path(__file__).parent)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Serving {DIRECTORY}")
        print(f"📍 Open: http://localhost:{PORT}/app.html")
        print(f"⏸️  Press CTRL+C to stop")
        httpd.serve_forever()
