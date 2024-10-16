import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Directory containing JSON files
JSON_DIR = "C:\\Users\\kroy2\\Documents\\python\\projects\\json_generate_test_files\\data"

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
        print(f"Searching for: {query}")
        results = self.search_json_files(query)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps(results)
        print(f"Sending response: {response}")
        self.wfile.write(response.encode())

    def search_json_files(self, query):
        results = []
        print(f"Searching in directory: {JSON_DIR}")
        try:
            for filename in os.listdir(JSON_DIR):
                if filename.endswith('.json'):
                    file_path = os.path.join(JSON_DIR, filename)
                    print(f"Checking file: {file_path}")
                    if query.lower() in filename.lower():
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            results.append({"filename": filename, "data": data})
                    else:
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            if self.match_query(data, query):
                                results.append({"filename": filename, "data": data})
        except Exception as e:
            print(f"Error searching files: {str(e)}")
        print(f"Found {len(results)} results")
        return results

    def match_query(self, data, query):
        query = query.lower()
        if isinstance(data, dict):
            return any(self.match_query(value, query) for value in data.values())
        elif isinstance(data, list):
            return any(self.match_query(item, query) for item in data)
        elif isinstance(data, str):
            return query in data.lower()
        else:
            return False

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SearchHandler)
    print(f"Server running on http://localhost:8000")
    httpd.serve_forever()