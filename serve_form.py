"""Simple HTTP Server to serve the job application form"""

import http.server
import socketserver
import os
from pathlib import Path

# Set the directory to serve files from
SERVE_DIR = Path(__file__).parent

PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SERVE_DIR), **kwargs)

# Create the server
Handler = MyHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"✅ Server running at http://localhost:{PORT}")
    print(f"📄 Job Application Form URL: http://localhost:{PORT}/job-application-form.html")
    print(f"Press CTRL+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n❌ Server stopped")
