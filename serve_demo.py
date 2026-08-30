import http.server
import socketserver
import os
import mimetypes

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/':
            path = '/index.html'
        
        # normalize file path
        rel_path = path.lstrip('/')
        file_path = os.path.join(DIRECTORY, rel_path.replace('/', os.sep))
        
        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, 'index.html')
            
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                mime_type, _ = mimetypes.guess_type(file_path)
                if not mime_type:
                    mime_type = 'text/html' if file_path.endswith('.html') else 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', mime_type + '; charset=utf-8' if 'text' in mime_type else mime_type)
                self.send_header('Content-Length', str(len(content)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, 'File not found')

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    with socketserver.TCPServer(('127.0.0.1', PORT), CustomHandler) as httpd:
        print(f'SERVER_ONLINE_ON_PORT_{PORT}')
        httpd.serve_forever()
