# 국가별 저소득층 복지 분석을 위한 모듈


def scrap(url: str, xpath=None, tag=None, cls_name=None):
	# xpath와 html tag, class name으로 웹크롤링
	try:
		from selenium import webdriver
		from bs4 import BeautifulSoup
	except ModuleNotFoundError as e:
		print(e)
	try:
		driver = webdriver.Chrome()
	except Exception:
		print(Exception)
	driver.get(url)
	
	# for naver
	article_title = []
	
	# for youtube
	video_title = []
	video_view = []

	# get title of youtube video
	if xpath is not None:
		driver.find_elements_by_xpath(xpath)
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		contents = bs.select('a#video-title')
		for video in contents: 
			video_title.append(video['title'])
		driver.close()
		return video_title
	
	# get headers of articles
	elif tag is not None:
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		contents = bs.findAll(tag, {'class': cls_name})
		for a in contents:
			article_title.append(a.text)

		# get click view of youtube video
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
	# text 형태소 분석
	try:
		import matplotlib.pyplot as plt
		import platform
		from konlpy.tag import Okt
		from collections import Counter
		from wordcloud import WordCloud
	except ModuleNotFoundError as e:
		print(e)

	# 검색어를 제외한 명사, 형용사, 동사 키워드 추출
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
	# 빈도수 높은 30개의 단어 추출
	frequency = Counter(wordlist).most_common(30)

	# 그래프 출력을 위한 운영체제별 한글 폰트 설정
	if platform.system() == 'Windows':
		path = r'c:\Windows\Fonts\malgun.ttf'
	elif platform.system() == 'Darwin':
		path = r'/System/Library/Fonts/AppleGothic'
	else:  # Linux
		path = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'

	# wordcloud 이미지 파일 저장 및 출력
	wc = WordCloud(font_path=path)
	wc = wc.generate_from_frequencies(dict(frequency))
	wc.to_file(f'{filename}.png')

	plt.figure(figsize=(10, 6))
	plt.axis('off')
	plt.imshow(wc)
	plt.show()
	plt.close()


def sendQuery(csv_file, hostname, username, passwd, dbname, tbname):
	# MySQL database에 query 업데이트
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
	
	# send "insert" query to database and close
	if db.rowcount == 0:
		for row in data:
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


def getData(hostname, username, passwd, dbname, tbname):
	# get data from MySQL database
	try:
		import pandas as pd
		import pymysql
	except ModuleNotFoundError as e:
		print(e)

	# connect to database
	conn = pymysql.connect(host=hostname, user=username,
						   password=passwd, database=dbname, charset='utf8')
	db = conn.cursor(pymysql.cursors.DictCursor)

	# execute query
	db.execute('USE ' + dbname)
	db.execute(f'SELECT * FROM {tbname}')

	# get data and close
	data = db.fetchall()
	data = pd.DataFrame(data)
	db.close()
	conn.close()
	return data


def plotGraph(data, title: str, xlabel: str, ylabel: str, filename: str):
	# make graph
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

	# save an img file, show and close the plot
	plt.savefig(f'{filename}', dpi=200)
	plt.show()
	plt.close()
