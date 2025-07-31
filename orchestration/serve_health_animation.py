#!/usr/bin/env python3
"""
Serve the animated health monitor web interface
"""

import http.server
import socketserver
import os
import webbrowser
from threading import Timer

PORT = 8888

class HealthAnimationServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}/health_animation.html')

if __name__ == "__main__":
    print(f"🏥 Venice Network Health Animation Server")
    print(f"=" * 50)
    print(f"Starting server on http://localhost:{PORT}")
    print(f"Opening browser to health animation...")
    print(f"\nPress Ctrl+C to stop the server")
    
    # Open browser after 1 second
    Timer(1.0, open_browser).start()
    
    # Start server
    with socketserver.TCPServer(("", PORT), HealthAnimationServer) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")