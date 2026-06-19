"""Simple HTTP Server to serve the job application form"""

import http.server
import socketserver
import os
from pathlib import Path

# Set the directory to serve files from
SERVE_DIR = Path(__file__).parent
PORT = 8081

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SERVE_DIR), **kwargs)

# Create the server
Handler = MyHTTPRequestHandler

if __name__ == '__main__':
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"✅ Server running at http://localhost:{PORT}")
            print(f"📄 Job Application Form URL: http://localhost:{PORT}/job-application-form.html")
            print(f"Press CTRL+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n❌ Server stopped")
    except OSError as e:
        print(f"❌ Error: {e}")
        print("Try a different port or close the process using that port")
