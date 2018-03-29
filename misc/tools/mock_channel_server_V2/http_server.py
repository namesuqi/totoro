# coding:utf-8
"""
由于办公室外网带宽有限，在测试seed多路供源时需要时播放端同时连接线上的P2P节点和本地的源站。
此脚本通过模拟channel server在收到SDK的起播请求后返回给SDK本地的src url和线上的file_id来解决这个问题
使用方法：将SDK的channel server指向本台机器的IP，其他服务器指向线上测试环境，随后播放线上的频道即可。

get_file_info.py:将select_file_info.py部署到远程机器上以获取数据信息，随后将select_file_info.py生成的file_info.json复制到本地并进行
处理。
select_file_info.py:被部署在远程机器上连接mysql的脚本，生成file_info.json文件
"""

from BaseHTTPServer import BaseHTTPRequestHandler
import json
from BaseHTTPServer import HTTPServer
import re
import get_file_info

# 为了避免本地源站遭受攻击，本地文件信息暂时手工配置

FILE_AVATAR_URL = "http://vodtest.crazycdn.com/test/Avatar_15Mbps.mp4"
FILE_AVATAR_SIZE = 1085532904

FILE_LIGHT_URL = "http://vodtest.crazycdn.com/test/demo_9mbps_oled_light.ts"
FILE_LIGHT_SIZE = 405924148

FILE_OCEAN_URL = "http://vodtest.crazycdn.com/test/Ocean_2mbps.ts"
FILE_OCEAN_SIZE = 172917700

FILE_PIANO_URL = "http://vodtest.crazycdn.com/test/piano.mp4"
FILE_PIANO_SIZE = 775134238

LOCAL_FILE_INFO = {FILE_AVATAR_SIZE: FILE_AVATAR_URL,
                   FILE_LIGHT_SIZE: FILE_LIGHT_URL,
                   FILE_OCEAN_SIZE: FILE_OCEAN_URL,
                   FILE_PIANO_SIZE: FILE_PIANO_URL}


# 使用正则匹配获取SDK启播url
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

# 调用det_file_info类的获取线上数据库中的频道信息
        gfi = get_file_info.get_file_info()
        file_info = gfi.get_file_info(file_url)

        file_id = file_info[u'file_id']
        file_size = int(file_info[u'fsize'])
        psize = int(file_info[u'psize'])
        file_ppc = int(file_info[u'ppc'])
        start_bitrate = int(file_info[u'start_bitrate'])
        limit_bitrate = int(file_info[u'limit_bitrate'])
        avg_bitrate = int(file_info[u'avg_bitrate'])
        cppc = 1
        cdn_url = LOCAL_FILE_INFO[int(file_info[u'fsize'])]

        body_data = {"file_id": file_id,
                     "fsize": file_size,
                     "psize": psize,
                     "ppc": file_ppc,
                     "start_bitrate": start_bitrate,
                     "limit_bitrate": limit_bitrate,
                     "avg_bitrate": avg_bitrate,
                     "cppc": cppc,
                     "src": {"type": "CDN", "url": cdn_url},
                     "token_url": cdn_url}

        # Just dump data to json, and return it

        message = json.dumps(body_data)

        self.send_response(200)

        self.send_header('Content-type', 'application/json')

        self.end_headers()

        self.wfile.write(message)


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 80), TodoHandler)
    print('Starting server, use to stop')
    server.serve_forever()
