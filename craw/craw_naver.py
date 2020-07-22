import requests
from bs4 import BeautifulSoup

#req = requests.get('https://tv.naver.com/r/', headers={'User-Agent': 'Mozilla/5.0'})
#raw = req.text
#naver_html = BeautifulSoup(raw, 'html.parser')
#infos = naver_html.select('div.cds')
#clip1 = infos[0]
#clip1_title = clip1.select_one('dt.title tooltip')
#print(clip1_title.text)
#print( infos[0].select_one('dt.title tooltip').text )

#for info in infos:
#	title = info.select_one('dt.title tooltip').text
#	print('제목은 ', title)

### 네이버 검색 내용 긁어오기 ####
#raw = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&query=%ED%99%8D%EC%BD%A9', headers={'User-Agent': 'Mozilla/5.0'}).text
#html = BeautifulSoup(raw, 'html.parser')
#news_list = html.select('.news .type01 > li')
#for news in news_list:
#	title = news.select_one('._sp_each_title').text
#	print('기사 제목들은 ', title)

### 네이버 검색 내용 페이지 이동하며 긁어오기 ####
#for page in range(3):	
#	raw = requests.get('https://search.naver.com/search.naver?&where=news&query=%ED%99%8D%EC%BD%A9&start=' + str(page*10+1), headers={'User-Agent': 'Mozilla/5.0'}).text
#	html = BeautifulSoup(raw, 'html.parser')
#	news_list = html.select('.news .type01 > li')
#	for news in news_list:
#		title = news.select_one('._sp_each_title').text
#		print('기사 제목들은 ', title)
#print('기사끝')


### 카카오 블로그 포스팅의 태그를 페이지 이동하며 긁어오기 ####
#for page in range(3):	 
#	raw = requests.get('https://tech.kakao.com/blog/page/'+str(page+1)+'/#posts', headers={'User-Agent': 'Mozilla/5.0'}).text
#	html = BeautifulSoup(raw, 'html.parser')
#	post_list = html.select('.wrap_post .list_post > li')
#	for post in post_list:
#		tag = post.select_one('.area_tag a').text
#		print('태그명은 ', title)
#print('태그명 수집 끝')


#### 네이버 주식정보에서 상위 주식 종목명 수집해오기 ####
#raw = requests.get('https://finance.naver.com/sise/lastsearch2.nhn', headers={'User-Agent': 'Mozilla/5.0'}).text
#html = BeautifulSoup(raw, 'html.parser')
#titles = html.select('.box_type_l .tltle')

#for each in titles:
#	name = each.text
#	print('종목명은 ', name)


#### 네이버 tv Top100 긁어오기 ####
#req = requests.get('http://tv.naver.com/r')
#raw = req.text
#html = BeautifulSoup(raw, 'html.parser')
#infos = html.select('div.cds')
#for info in infos:
#	title = info.select_one('tooltip').text
#	chn = info.select_one('dd.chn > a').text
#	hit = info.select_one('span.hit').text
#	like = info.select_one('span.like').text
#	print(chn, '/', title, '/', hit, '/', like)


#### 파이썬의 데이터구조, 딕셔너리 활용하기
#json과 객체 형태와 흡사하다.
#print(people.keys())
#print(people.values())
#print(people.items())
#chn_infos = {'하트시그널2': {'hit': 20000, 'like': 3800},
#            '미스터션샤인': {'hit': 18000, 'like': 3500},
#            '쇼미더머니7': {'hit': 25000, 'like': 2200}}
#for each_chn in chn_infos.items():
#	print( each_chn[0], '의 조회수는', each_chn[1]['hit'], '입니다')

#### 파이썬의 딕셔너리를 활용하여 네이버 tv 데이터를 구조화하기

#req = requests.get('http://tv.naver.com/r')
#raw = req.text
#html = BeautifulSoup(raw, 'html.parser')

#page_infos = html.select('div.cds')
#ch_infos = {}

# 체널명을 키값으로 구조화하기
#for ch in page_infos:
#	ch_name = ch.select_one('dd.chn > a').text
#	ch_infos[ch_name] = {'hit': 0, 'like': 0}

# 체널명을 기준으로 조회수, 좋아요 데이터 값 쌓아주기
#for info in page_infos:
#	ch_name = info.select_one('dd.chn > a').text
#	hit = info.select_one('span.hit').text[4:].replace(',','')
#	like = info.select_one('span.like').text[5:].replace(',','')
#	ch_infos[ch_name]['hit'] += int(hit)
#	ch_infos[ch_name]['like'] += int(like)
	
#print( ch_infos )

#### 위 예제를 if-else 구문을 이용해서 축약해보기 ####
req = requests.get('http://tv.naver.com/r')
raw = req.text
html = BeautifulSoup(raw, 'html.parser')

page_infos = html.select('div.cds')
ch_infos = {}

for info in page_infos:
	ch_name = info.select_one('dd.chn > a').text
	hit = info.select_one('span.hit').text[4:].replace(',','')
	like = info.select_one('span.like').text[5:].replace(',','')
	score = (int(hit)+int(like)*350)/100

	if ch_name in ch_infos.keys():
		ch_infos[ch_name]['hit'] += int(hit)
		ch_infos[ch_name]['like'] += int(like)
		ch_infos[ch_name]['score'] += score
	else:
		ch_infos[ch_name] = {'hit': int(hit), 'like': int(like), 'score': score}

#print(ch_infos) 


#### 파이썬의 sorted() 함수 ####
#리스트를 인자로 넘기면 오름차순으로 정렬해준다, 알파벳 숫자 혼합은 불가능
#딕셔너리 타입을 인자로 넘길경우 키 값만 뽑아서 리스트화한다
#이를 피하기 위해서는 딕셔너리 타입을 items() 함수로 튜플화해 넘긴다
#scores = {'h': 16, 'b': 24, 'd': 91, 'c': 138, 'z': 6, 'a': 65}

#이때 키 값이 아닌 value 값을 기준으로 정렬하고 싶을때는
#튜플을 넘기면 value 값을 리턴하는 사용자 정의함수를 정의하고
#이 함수를 sorted()함수의 key 속성 값, 즉 정렬함수로서 전달해주면 된다
#이를 통해 sorted() 함수는 어떤 것을 기준으로 하여 정렬할지 전달받게 된다.
#def sortKey(item):
#	return item[1]
#만약 내림차순으로 정렬하고자 하면 reverse 속성값을 True로 해주면 된다.
#print(sorted(scores.items(), key=sortKey, reverse=True))


#### 위 네이버 tv 예제에서 수집한 데이터를 조회수나 점수 기준으로 정렬해본다 ####
def sort_by_hit(item): 
	return item[1]['hit']
def sort_by_score(item):
	return item[1]['score']
sorted_list = sorted(ch_infos.items(), key=sort_by_score, reverse=True)

#for sort_item in sorted_list:
#	print('체널명:', sort_item[0], '\t점수는:', sort_item[1]['score'], '\t조회수:', sort_item[1]['hit'], '\t좋아요:', sort_item[1]['like'])

#### python으로 파일을 생성하고, 읽고, 데이터 저장해보기 ####
#w:새로 작성, r:읽기, a: 추가
#f는 파일 클래스의 변수로 지정된다
#f = open('test.txt', 'w')
#.write() 함수는 매개변수로 전달된 문자열을 파일에 쓰는 역할
#f.write('Learning data crawling')
#.close() 함수는 열었던 파일을 닫아 더 이상 컨트롤할 수 없게 만든다.
#사용이 끝난 파일은 꼭 close()함수를 사용해 연결을 종료해야한다.
#f.close()

#f = open('test.txt', 'a')
#f.write('\nThis\nis\nstage5')
#f.close()

#### 네이버 tv 예제를 데이터 형식으로 저장해보기 ####
#f = open('naver_tv_top.csv', 'w')
#for sort_item in sorted_list:
#	f.write('체널명:' + str(sort_item[0]) + '\t점수는:' + str(sort_item[1]['score']) + '\t조회수:' + str(sort_item[1]['hit']) + '\t좋아요:' + str(sort_item[1]['like']) + '\n')
#f.close

#### 데이터를 매일 날짜 별로 저장해보기 ####
import datetime
dt = datetime.datetime.now()
file_name = 'naver_tv_top_'+ dt.strftime('%Y_%m_%d')
f = open(file_name+'.csv', 'w')
for sort_item in sorted_list:
	f.write('체널명:' + str(sort_item[0]) + '\t점수는:' + str(sort_item[1]['score']) + '\t조회수:' + str(sort_item[1]['hit']) + '\t좋아요:' + str(sort_item[1]['like']) + '\n')
f.close


import openpyxl
excel = openpyxl.Workbook()
clips_sheet = excel.active
clips_sheet.title = "네이버 TV TOP 100"
by_hits_sheet = excel.create_sheet('조회수별 정렬')
clips_sheet.append(['체널명','클립 제목', '조회수', '좋아요'])
by_hits_sheet.append(['체널명','가중치 점수', '조회수 합', '좋아요 합'])

for info in page_infos:
	ch_name = info.select_one('dd.chn > a').text
	title =  info.select_one('.title tooltip').text
	hit = info.select_one('span.hit').text[4:].replace(',','')
	like = info.select_one('span.like').text[5:].replace(',','')
	clips_sheet.append([ch_name,title,hit,like])

for sort_item in sorted_list:
	by_hits_sheet.append([sort_item[0], sort_item[1]['score'], sort_item[1]['hit'], sort_item[1]['like'] ])

excel.save(file_name+'.xlsx')
excel.close()




