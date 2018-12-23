# Author: CG
# comment.bilibili.com/{cid}.xml  danmuku
# https://www.bilibili.com/video/{av}
# https://www.bilibili.com/bangumi/play/{ep}

from urllib import request


import gzip
from zlib import decompress
import zlib
import codecs
import re



def fetch(url):
    res = request.urlopen(request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
    }))
    content = res.read()
    if res.headers['Content-Encoding'] == 'gzip':
        return gzip.decompress(content).decode()
    elif res.headers['Content-Encoding'] == 'deflate':
        return decompress(content, -zlib.MAX_WBITS).decode()
    else:
        return content.decode()

def write_utf8(path, data):
    with codecs.open(path, 'w+', 'utf-8') as f: 
        f.write(data)

content_url = 0

id = input('请输入ep号或av号（例如ep14774）：')
if id.startswith('ep'):
    content_url = 'https://www.bilibili.com/bangumi/play/' + id
elif id.startswith('av'):
    content_url = 'https://www.bilibili.com/video/' + id
else:
    exit()

content = fetch(content_url)

# title 
title = re.search('<title[^>]*>(.*?)</title>', content)

r = re.search('(?<="cid":).*?(?=,)', content)
print('cid: ' + r.group())

danmuku_url = 'https://comment.bilibili.com/'+ r.group() +'.xml'

danmu = fetch(danmuku_url)


print(title.group(1))

write_utf8('./' + title.group(1) + '.xml', danmu)
