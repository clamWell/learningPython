import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

rank_array = {}

#### selenium 이용해 네이버 실시간 검색 DB에 접근 ####
driver = webdriver.Chrome("./chromedriver")
driver.get("https://datalab.naver.com/keyword/realtimeList.naver?datetime=2019-09-27T11%3A00%3A00&where=main")

page = 1
while page < 20:	
	rank_date = driver.find_element_by_css_selector(".section_serch_area .date_indo .date_box .date_txt").text[:-4].replace('.','')
	rank_data = driver.find_elements_by_class_name("keyword_rank")
	rank_age_all = rank_data[0]
	rank_list = rank_age_all.find_elements_by_class_name("list")
	print(rank_date, '급상승검색어\n')
	
	rank_array[rank_date] = []

	for each_rank in rank_list:
		rank_num = each_rank.find_element_by_css_selector("em.num").text
		rank_text = each_rank.find_element_by_css_selector("span.title").text
		#print(rank_num, ', ', rank_text)
		rank_array[rank_date].append(str(rank_num)+','+str(rank_text))
	
	print(rank_date, '끝\n\n\n') 
	page = page + 1
	time.sleep(1)
	try:
		driver.find_element_by_css_selector(".section_serch_area .date_indo ._prev_day").click()
	except:
		break

print("\n크롤링 끝")
driver.close()

import datetime
dt = datetime.datetime.now()

file_name = 'naver_keyword_top'+ dt.strftime('%Y_%m_%d')
f = open(file_name+'.csv', 'w')
for rank_item in rank_array.items():
	rank_ltem_list = rank_item[1]
	for i in rank_ltem_list:
		f.write(rank_item[0]+','+str(i)+'\n')
f.close