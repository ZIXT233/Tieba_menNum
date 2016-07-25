# -*- coding:utf-8-*-
import urllib.request, urllib.parse
import json
from flask import Flask

app = Flask(__name__)
tieba_name = ['minecraft', 'minecraftpe', 'minecraft图文', 'minecraft联机', '红石电路']

def get_urls(tieba):
    urls = dict()
    for key in tieba:
        tieba_name_in_url = ''
        for uchar in key:
            if '\u4e00' <= uchar <= '\u9fff': #处理中文部分
                tieba_name_in_url += urllib.parse.quote(uchar)
            else:
                tieba_name_in_url += uchar
        urls[key] = 'http://tieba.baidu.com/mo/' \
                    'q---8EAD9A52B0D0DF103FBB79BAA0FA7D56%3AFG%3D1-sz%40320_240%2C,-2-3-0--2/' \
                    'm?kw=' + tieba_name_in_url
    return urls

def get_menNum(page):
    start_index = page.find('<span class="info_value">') + len('<span class="info_value">')
    end_index = page.find('</span>', start_index)
    return int(page[start_index:end_index])

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/mi')
def mi():
    urls = get_urls(tieba_name)
    data = dict()
    for tieba, url in urls.items():
        fp = urllib.request.urlopen(url)
        page = fp.read()
        men_Num = get_menNum(page.decode('utf-8'))
        data[tieba] = str(men_Num)
    return json.dumps(data, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

