#!/usr/bin/python3

import urllib.request, urllib.parse, urllib.error
import json
import time
import collections
import codecs
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
endpoint_url = 'https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search'
query_args = {  'q':'初音ミク',
                'targets':'title',
                'fields':'contentId,title,viewCounter,commentCounter,mylistCounter',
                'filters[viewCounter][gte]':'10000',
                '_sort':'-viewCounter',
                '_offset':'0',
                '_limit':'100',
                '_context':'name'
                }
encoded_args = urllib.parse.urlencode(query_args)
print("Content-Type: text/html; charset=utf-8")
print("")
#print('Encoded:', encoded_args)
global response
try:
    response = urllib.request.urlopen(endpoint_url + '?' + encoded_args).read().decode("utf-8")
#   print(response)
except urllib.error.URLError as error:
    print(error)
ret = {}
line_count = 0
for i, line in enumerate(response.splitlines()):
    data = json.loads(line)
    if data['meta']['status'] != 200:
        if data['meta']['status'] == 400:
            print('不正なパラメータです')
        elif data['meta']['status'] == 500:
            print('検索サーバの異常です')
        elif data['meta']['status'] == 503:
            print('サービスがメンテナンス中です');
        else:
            print('何らかのエラーです');
    elif data['meta']['status'] == 200:
        for movie_data in data['data']:
            ret[line_count] = movie_data
            line_count+=1
        continue
print('<!DOCTYPE HTML>')
print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print('<meta http-equiv="content-language" content="ja"> ')
print('<link rel="author" href="mailto:mail@mail.com">')
print('<link rel="stylesheet" type="text/css" href="sample.css">')
print('<title lang="ja">NicoNicoRanking文字コードテスト</title>')
print('</head>')
print('<body>')
print('<header class="select_header">')
print('<div class="menu">')
print('<select name="startTime">')
print('<option value="1">24時間</option>')
print('<option value="2">03日間</option>')
print('<option value="3">01週間</option>')
print('<option value="4">01月間</option>')
print('<option value="5">03月間</option>')
print('<option value="6">09月間</option>')
print('<option value="7">03年間</option>')
print('</select>')
print('<ul class="menu_text">')
print('<li class="menu_item"><a href="#item1">001-050</a></li>')
print('<li class="menu_item"><a href="#item2">051-100</a></li>')
print('<li class="menu_item"><a href="#item3">101-150</a></li>')
print('<li class="menu_item"><a href="#item4">151-200</a></li>')
print('<li class="menu_item"><a href="#item5">201-250</a></li>')
print('<li class="menu_item"><a href="#item5">251-300</a></li>')
print('</ul>')
print('</div>')
print('</header>')
print('<div class="main">')
print('<div class="box" id="menu01">')
for i in range(3):
    print('<br>')
for i, data2 in enumerate(ret.values()):
    id = data2['contentId']
    print('<p>{}</p>'.format(id))
    print('<p>{}</p>'.format('<img src="http://tn.smilevideo.jp/smile?i=' + id[2::] + '">'))
    print('<p>{}</p>'.format(data2['title']))
    print('<p>{}</p>'.format('総合' + str(data2['viewCounter'] + data2['commentCounter'] + 15 * data2['mylistCounter'])))
    print('<p>{}</p>'.format('再生' + str(data2['viewCounter'])))
    print('<p>{}</p>'.format('マイ' + str(data2['mylistCounter'])))
    print('<p>{}</p>'.format('コメ' + str(data2['commentCounter'])))

print('</div>')
print('</div>')
print('</body>')
print('</html>')
