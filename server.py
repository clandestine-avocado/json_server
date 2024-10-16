import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Directory containing JSON files
JSON_DIR = "C:\Users\kroy2\Documents\python\projects\json_generate_test_files\data"

class SearchHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/search'):
            self.handle_search()
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

    def handle_search(self):
        query = parse_qs(urlparse(self.path).query).get('q', [''])[0]
        results = self.search_json_files(query)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(results).encode())

    def search_json_files(self, query):
        results = []
        for filename in os.listdir(JSON_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(JSON_DIR, filename), 'r') as file:
                    data = json.load(file)
                    if self.match_query(data, query):
                        results.append(data)
        return results

    def match_query(self, data, query):
        query = query.lower()
        for value in data.values():
            if isinstance(value, str) and query in value.lower():
                return True
        return False

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SearchHandler)
    print(f"Server running on http://localhost:8000")
    httpd.serve_forever()