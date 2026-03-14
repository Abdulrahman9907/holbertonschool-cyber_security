#!/usr/bin/env python3
"""
Local HTTP server that extension calls to perform git operations.
Runs on localhost:9999
"""

import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import os

project_dir = Path(r"C:\Users\Admin\Documents\projects\holbertonschool-cyber_security")

class GitHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/git-push':
            # Push code with message 'a'
            try:
                os.chdir(project_dir)
                subprocess.run(['git', 'add', '-A'], capture_output=True, timeout=10)
                result = subprocess.run(['git', 'commit', '-m', 'a'],
                                      capture_output=True, text=True, timeout=10)
                subprocess.run(['git', 'push'], capture_output=True, timeout=20)

                response = {
                    'success': True,
                    'message': 'Code pushed with commit "a"'
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                response = {
                    'success': False,
                    'message': str(e)
                }
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

if __name__ == '__main__':
    print(f'[SERVER] Starting extension server on localhost:9999')
    print(f'[SERVER] Project dir: {project_dir}')
    print(f'[SERVER] Keep this running while using the extension')

    server = HTTPServer(('localhost', 9999), GitHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n[SERVER] Shutting down')
        server.shutdown()
