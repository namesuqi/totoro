# coding=utf-8
# coding = utf-8
from BaseHTTPServer import BaseHTTPRequestHandler
import json
from BaseHTTPServer import HTTPServer
import re
import MySQLdb
import time




# config
PSIZE = 1392
START_BIT_RATE = 10000000
LIMIT_BIT_RATE = 20000000
AVG_BIT_RATE = 2305305
CPPC = 1

FILE1_URL = "http://migu.x.00cdn.com/demo/4k/piano.mp4"
FILE1_CDN_URL = "http://vodtest.crazycdn.com/test/piano.mp4"
FILE1_ID = "C774E9CA0A9D4D069AC34ECA121955C4"
FILE1_SIZE = 775134238
FILE1_PPC = 304

FILE2_URL = "http://c23.myccdn.info/a6d33f8c1bc5dbf00e5b1125d4c62ceb/5a87af7a/mp4/Avatar_15Mbps.mp4"
FILE2_CDN_URL = "http://vodtest.crazycdn.com/test/Avatar_15Mbps.mp4"
FILE2_ID = "E9FF088495D040528F218F1B046F982D"
FILE2_SIZE = 1085532904
FILE2_PPC = 256

FILE3_URL = "http://c23.myccdn.info/076c9b0081204412b0346d9beb486923/5abc4f25/mp4/Ocean_2mbps.ts"
FILE3_CDN_URL = "http://vodtest.crazycdn.com/test/Ocean_2mbps.ts"
FILE3_ID = "80E855957F404713A32222DF6531F64C"
FILE3_SIZE = 172917700
FILE3_PPC = 32

MOCK_STRATEGY = {FILE1_CDN_URL: (FILE1_CDN_URL, FILE1_ID, FILE1_SIZE, FILE1_PPC),
                 FILE2_CDN_URL: (FILE2_CDN_URL, FILE2_ID, FILE2_SIZE, FILE2_PPC),
                 FILE3_CDN_URL: (FILE3_CDN_URL, FILE3_ID, FILE3_SIZE, FILE3_PPC)
                 }

# class File():
#     def __init__(self):
#         self.


def find_url(path):
    pattern = re.compile(r'.*url=(.*)')
    match = pattern.match(path)
    return match.group(1)


class TodoHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        file_url = find_url(self.path)
        file_url = file_url.replace('%3a', ':')
        file_url = file_url.replace('%2f', '/')

        print file_url

        cdn_url = MOCK_STRATEGY.get(file_url)[0]
        file_id = MOCK_STRATEGY.get(file_url)[1]
        file_size = MOCK_STRATEGY.get(file_url)[2]
        file_ppc = MOCK_STRATEGY.get(file_url)[3]

        body_data = {"file_id": file_id,
                     "fsize": file_size,
                     "psize": PSIZE,
                     "ppc": file_ppc,
                     "start_bitrate": START_BIT_RATE,
                     "limit_bitrate": LIMIT_BIT_RATE,
                     "avg_bitrate": AVG_BIT_RATE,
                     "cppc": CPPC,
                     "src": {"type": "CDN", "url": cdn_url},
                     "token_url": cdn_url}

        # Just dump data to json, and return it

        message = json.dumps(body_data)

        self.send_response(200)

        self.send_header('Content-type', 'application/json')

        self.end_headers()

        self.wfile.write(message)


if __name__ == '__main__':
    # Start a simple server, and loop forever
    server = HTTPServer(('0.0.0.0', 80), TodoHandler)
    print('Starting server, use to stop')
    server.serve_forever()
