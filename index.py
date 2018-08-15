#!C:\python37\python.exe

# -*- coding:utf-8 -*-


#上のパスはWindows環境でPythonのインストールフォルダ
#pyファイルはUTF-8、改行はCR+LFで保存
#pythonのバージョンは3.7(3系)、2系だと動かないので注意


import urllib.request, urllib.parse, urllib.error
import json
import time
import collections
import codecs
import sys
#下はPythonは文字化けで泣かされるので、Webで見つけたおまじない
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


#ブラウザに文字を出力する時のおきまり
print("Content-Type: text/html; charset=utf-8")
print("")

#HTTPで動画のデータを取得する前の準備
endpoint_url = 'http://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search'
query_category = '初音ミク'
query_target = 'tagsExact'
query_offset = 1900
query_limit = 50
query_startTime = ''
category_temp = ['エンターテイメント OR 音楽 OR 歌ってみた OR 演奏してみた OR 踊ってみた OR VOCALOID OR ニコニコインディーズ',
'動物 OR 料理 OR 自然 OR 旅行 OR スポーツ OR ニコニコ動画講座 OR 車載動画 OR 歴史',
'政治',
'科学 OR ニコニコ技術部 OR ニコニコ手芸部 OR 作ってみた',
'アニメ OR ゲーム OR 実況プレイ動画 OR 東方 OR アイドルマスター OR ラジオ OR 描いてみた',
'日記 OR その他 OR 例のあれ']


for rank_num in range(6):
	query_offset = 50 * rank_num
	query_limit  = 50

	#データを取得、取得したデータの内で動画のデータだけ選ぶ
	ret = [[], [], [], [], [], []]
	for http_i in range(6):
		query_category = category_temp[http_i]
		query_args = {	'q':query_category,
						'targets':query_target,
						'fields':'contentId,title,viewCounter,commentCounter,mylistCounter',
						'filters[viewCounter][gte]':'1',
						'_sort':'-viewCounter',
						'_offset':'' + str(query_offset),
						'_limit':'' + str(query_limit),
						'_context':'name'
					}
		encoded_args = urllib.parse.urlencode(query_args)
	#	print('Encoded:', encoded_args)

		try:
			response = urllib.request.urlopen(endpoint_url + '?' + encoded_args).read().decode("utf-8")
	#		print(response)
		except urllib.error.URLError as error:
			print(error)
		
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
					ret[http_i].append(movie_data)
					#print(ret[http_i])
					line_count+=1
				continue


	#取得したデータの順番の入れ替え
	data3 = [0 for col in range(300)]
	for i in range(6):
		for j, data in enumerate(ret[i]):
			data3[j * 6 + i] = data


	#HTMLのファイルの前半部分、'''～'''で囲まれた部分は文字列として扱われる
	html_rink = ['./ranking0.html', './ranking1.html', './ranking2.html', './ranking3.html', './ranking4.html', './ranking5.html']
	html_text1 = f'''
	<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<meta http-equiv="content-language" content="ja"> 
		<link rel="author" href="mailto:mail@mail.com">
		<link rel="stylesheet" type="text/css" href="sample5.css">
		<title lang="ja">NicoNicoRankingテスト</title>
	</head>
	<body>
		<header class="select_header">
			<div class="menu">
				<select name="startTime">
					<option value="1">24時間</option>
					<option value="2">03日間</option>
					<option value="3">01週間</option>
					<option value="4">01月間</option>
					<option value="5">03月間</option>
					<option value="6">09月間</option>
					<option value="7">03年間</option>
				</select>
				<ul class="menu_text">
					<li class="menu_item"><a href="{html_rink[0]}">001-050</a></li>
					<li class="menu_item"><a href="{html_rink[1]}">051-100</a></li>
					<li class="menu_item"><a href="{html_rink[2]}">101-150</a></li>
					<li class="menu_item"><a href="{html_rink[3]}">151-200</a></li>
					<li class="menu_item"><a href="{html_rink[4]}">201-250</a></li>
					<li class="menu_item"><a href="{html_rink[5]}">251-300</a></li>
				</ul>
			</div>
		</header>

		<div class="main">
		<p><br></p>
		<p><br></p>
		<p><br></p>
	'''


	#HTMLのファイルの中盤、動画の画像、題名、数値の部分
	html_text2 = ['' for col in range(300)]
	for i, data2 in enumerate(data3):
		if data2 == 0:
			id = '0'
			title = '該当なし'
			v_counter = 0
			c_counter = 0
			m_counter = 0
		else:
			movie_id = data2['contentId']
			image_url = 'http://tn.smilevideo.jp/smile?i=' + movie_id[2::]
			title = data2['title']
			v_counter = str(data2['viewCounter'])
			c_counter = str(data2['commentCounter'])
			m_counter = str(data2['mylistCounter'])
		
		
		html_text2[i] = f'''
		<div class="box">
		
		<div class="image"><p><img src="{image_url}"></p></div>
		<div class="text"><p>{title}</p></div>
		
		<div class="point" style="align-self:flex-end;">
		
		<div class="point1">
		<p>
		<div class="point2">再生数</div>
		<div class="point3">コメント</div>
		<div class="point3">マイリス</div>
		</p>
		</div>
		
		<div class="point1">
		<p>
		<div class="point4">{v_counter}</div>
		<div class="point5">{c_counter}</div>
		<div class="point5">{m_counter}</div>
		</p>
		</div>
		
		</div>
		
		</div>
		'''


	#HTMLのファイルの後半部分
	html_text3 = '''
		</div>
	</body>
	</html>
	'''


	#取得したデータをHTMLファイルに保存
	html_file = codecs.open('ranking' + str(rank_num) + '.html',"w",'utf-8')
	html_file.write(html_text1)
	for text in html_text2:
		html_file.write(text)
	html_file.write(html_text3)
	html_file.close()
