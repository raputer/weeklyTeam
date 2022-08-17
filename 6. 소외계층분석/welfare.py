# 국가별 저소득층 복지 분석을 위한 모듈

"""scrap(url, xpath, tag, cls_name)
Scrap by a given xpath or a html tag with class name

[parameter]
url : url address
xpath : xpath value
tag : html tag value
cls_name : html tag's class name
"""
def scrap(url: str, xpath=None, tag=None, cls_name=None):
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


"""mkWordCloud(context, except_kwrd, filename)
Make WordCloud image

[parameter]
context : string list of text
except_kwrd : keyword list has to be excepted from context
filename : png file name
"""
def mkWordCloud(context=None, except_kwrd=None, filename='wcimg'):
	try:
		import matplotlib.pyplot as plt
		import platform
		from konlpy.tag import Okt
		from collections import Counter
		from wordcloud import WordCloud
	except ModuleNotFoundError as e:
		print(e)

	# hangeul font path by OS
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
	plt.close()


"""sendQuery(csv_file, hostname, username, passwd, dbname, table_name)
Send queries to database by csv file

[parameter]
csv_file : [csv file path + ] csv file name
hostname : database host name 
username : database user name
passwd database password
dbname : database name
tbname : database table name
"""
def sendQuery(csv_file, hostname, username, passwd, dbname, tbname):
	try:
		import pymysql
		import csv
		from pymysql import OperationalError
	except ModuleNotFoundError as e:
		print(e)

	# open and read csv data
	file = open(csv_file, mode='r', encoding='utf-8')
	data = csv.reader(file)
	header = next(data)

	# connect to MySQL DB
	conn = pymysql.connect(host=hostname, user=username,
						   password=passwd, database=dbname, charset='utf8')
	db = conn.cursor(pymysql.cursors.DictCursor)
	db.execute('USE '+dbname)
	
	# send <insert into ~ values> queries
	if db.rowcount == 0:
		for row in data:
			row = str(row).lstrip('[')
			row = row.rstrip(']')
			db.execute('set foreign_key_checks=0')
			try:
				db.execute(f'INSERT INTO {tbname}({", ".join(header)}) VALUES ({row})')
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


"""getData(hostname, username, passwd, dbname, tbname)
Get data from database and return pandas DataFrame object

[parameter]
hostname : database host name
username : database user name
passwd : database password
dbname : database name
tbame : database table name
"""
def getData(hostname, username, passwd, dbname, tbname):
	try:
		import pandas as pd
		import pymysql
	except ModuleNotFoundError as e:
		print(e)

	conn = pymysql.connect(host=hostname, user=username,
						   password=passwd, database=dbname, charset='utf8')
	db = conn.cursor(pymysql.cursors.DictCursor)
	db.execute('USE '+dbname)
	db.execute(f'SELECT * FROM {tbname}')
	data = db.fetchall()
	data = pd.DataFrame(data)
	db.close()
	conn.close()
	return data


"""plotGraph(data, title, xlabel, ylabel, filename)
Show plot graph and save a png file

[parameter]
data : pandas DataFrame object
title : title on a plot graph
xlabel : xlabel on a plot graph
ylabel : ylabel on a plot graph
filename : img file name for save
"""
def plotGraph(data, title: str, xlabel: str, ylabel: str, filename: str):
	try:
		import platform
		import matplotlib.pyplot as plt
	except ModuleNotFoundError as e:
		print(e)

	# hangeul font settings on the graph by OS
	if platform.system() == 'Windows':
		plt.rc('font', family='Malgun Gothic')
	elif platform.system() == 'Darwin':
		plt.rc('font', family='AppleGothic')
	else:
		plt.rc('font', family='NanumMyeongjo')

	plt.figure(figsize=(10, 6), layout='constrained')
	for i in range(len(data)):
		plt.plot(data.iloc[i])
	
	# optional settings
	plt.title(title, size=20, pad=10)
	plt.margins(0.1)
	plt.xticks(rotation=45)
	plt.xlabel(xlabel, size=15)
	plt.ylabel(ylabel, size=15)
	plt.legend(data.index, loc=2)

	# save a img file, show and close the plot
	plt.savefig(f'{filename}', dpi=200)
	plt.show()
	plt.close()