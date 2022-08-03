"""고용, 임금으로 알아본 국가별 저소득층 복지 분석을 위한 모듈"""


def scrap(url: str, xpath=None, tag=None, cls_name=None):
	"""webscraping by a given xpath or a html tag with class name"""
	try:
		from selenium import webdriver
		from bs4 import BeautifulSoup
	except ModuleNotFoundError as e:
		print(e)
	try:
		driver = webdriver.Chrome()
	except FileNotFoundError as e:
		print('cannot excute chrome broswer')
		print(e)
	driver.get(url)
	
	article_title = []
	video_title = []
	video_view = []

	# get youtube video title
	if xpath is not None:
		driver.find_elements_by_xpath(xpath)
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		contents = bs.select('a#video-title')
		for video in contents: 
			video_title.append(video['title'])
		driver.close()
		return video_title
	
	elif tag is not None:
		# get naver article headers
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		contents = bs.findAll(tag, {'class': cls_name})
		for a in contents:
			article_title.append(a.text)

		# get youtube video click view
		# (조회수 33만회, 2개월) -> 33 
		for info in contents:
			info = info.text
			if info.startswith('조회수'):
				info = info.split()[1]
				info = info.replace('만회', '')
				video_view.append(int(info))
		driver.close()
		return article_title, video_view


def mkWordCloud(context=None, except_kwrd=None, filename='wcimg'):
	"""make WordCloud image
	context : text string list
	except_kwrd : keyword list has to be excepted from context
	filename : png file name
	"""
	try:
		import matplotlib.pyplot as plt
		import platform
		from konlpy.tag import Okt
		from collections import Counter
		from wordcloud import WordCloud
	except ModuleNotFoundError as e:
		print(e)

	# hangeul font path
	if platform.system() == 'Windows':
		path = r'c:\Windows\Fonts\malgun.ttf'
	elif platform.system() == 'Darwin':  # Mac
		path = r'/System/Library/Fonts/AppleGothic'
	else:  # Linux
		path = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'

	# extract keyword list except the search keyword
	okt = Okt()
	wordlist = []
	for text in context:
		for key in except_kwrd:
			if key in text:
				text = text.replace(key, '')
				for word, tag in okt.pos(text):
					if tag in ['Noun', 'Adjective', 'Verb']:
						if key not in word:
							wordlist.append(word)
	frequency = Counter(wordlist).most_common(30)

	# save and display wordcloud image
	wc = WordCloud(font_path=path)
	wc = wc.generate_from_frequencies(dict(frequency))
	wc.to_file(f'{filename}.png')

	plt.figure(figsize=(10, 6))
	plt.axis('off')
	plt.imshow(wc)
	plt.show()


def sendQuery(csv_file, hostname, username, passwd, dbname, table_name):
	"""send insert queries to database by csv file"""
	# open and read csv data
	try:
		import pymysql
		import csv
		from pymysql import OperationalError
	except ModuleNotFoundError as e:
		print(e)
	file = open(csv_file, mode='r', encoding='utf-8')
	data = csv.reader(file)
	header = next(data)

	# connect to MySQL DB
	conn = pymysql.connect(host=hostname, user=username,
						   password=passwd, database=dbname, charset='utf8')
	db = conn.cursor(pymysql.cursors.DictCursor)
	db.execute('USE '+dbname)
	
	# send insert queries
	if db.rowcount == 0:
		for row in data:
			row = str(row).lstrip('[')
			row = row.rstrip(']')
			db.execute('set foreign_key_checks=0')
			try:
				db.execute(f'INSERT INTO {table_name}({", ".join(header)}) VALUES ({row})')
			except OperationalError as e:
				print(e)
				file.close()
				db.close()
				conn.close()
			db.execute('set foreign_key_checks=1')
			db.connection.commit()
	file.close()
	db.close()
	conn.close()


def getData(hostname, username, passwd, dbname, table_name):
	"""return pandas DataFrame from database"""
	try:
		import pandas as pd
		import pymysql
	except ModuleNotFoundError as e:
		print(e)

	conn = pymysql.connect(host=hostname, user=username,
						   password=passwd, database=dbname, charset='utf8')
	db = conn.cursor(pymysql.cursors.DictCursor)
	db.execute('USE '+dbname)
	db.execute(f'SELECT * FROM {table_name}')
	data = db.fetchall()
	data = pd.DataFrame(data)
	db.close()
	conn.close()
	return data


def plotgraph(data, title, xlabel, ylabel, save_name):
	try:
		import numpy as np
		import platform
		import matplotlib.pyplot as plt
		from matplotlib import font_manager as fm, rc
	except ModuleNotFoundError as e:
		print(e)

	if platform.system() == 'Windows':
		font_fname = r'c:\Windows\Fonts\malgun.ttf'
	elif platform.system() == 'Darwin':
		font_fname = r'/System/Library/Fonts/AppleGothic'
	else:
		font_fname = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'

	font_family = fm.FontProperties(fname=font_fname).get_name()
	plt.rcParams['font.family']=font_family

	plt.figure(figsize=(10, 6), layout='constrained')
	for i in range(len(data)):
		plt.plot(data.iloc[i])
	plt.title(title, fontsize=20, pad=10)
	plt.margins(0.1)
	plt.xticks(rotation=45)
	plt.xlabel(xlabel, fontsize=15)
	plt.ylabel(ylabel, fontsize=15)
	plt.legend(data.index, loc=2);
	# plt.savefig(f'{save_name}', dpi=200);