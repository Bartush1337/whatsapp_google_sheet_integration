import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import google_sheet_pusher
import message_parser
import json

interesting_groups = ["טרמפיסטים #2 עוזרים לחיילים", "טרמפיסטים 1# עוזרים לחיילים", "Test"]
par = message_parser.MessageParser()
config = json.load(open("config.json", "rb"))
sheet_pusher = google_sheet_pusher.SpreadSheetCommunicator(config)

class S(BaseHTTPRequestHandler):
    def _set_response(self, response=200):
        self.send_response(response)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        body = json.loads(post_data.decode('utf-8'))
        response = http.client.OK
        if body["group_name"] in interesting_groups:
            response = self.handle_message(body["message"])
        else:
            print("group {} not interesting".format(body["group_name"]))
        self._set_response(response)
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def handle_message(self, message):
        response = http.client.OK
        try:
            message_dict = par.pattern_match(message)
        except Exception:
            message_dict = {'error': True, 'raw_data' : message}
            response = http.client.NOT_ACCEPTABLE
        logging.info(f"Parsed message: {message_dict}")
        sheet_pusher.communicate_message(message_dict)
        return response

def run(server_class=HTTPServer, handler_class=S, port=2001):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()