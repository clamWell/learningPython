import requests
from bs4 import BeautifulSoup

#### selenium 이용해 네이버 맵에서 검색하기

from selenium import webdriver
import time

driver = webdriver.Chrome('./chromedriver')
driver2 = webdriver.Chrome('./chromedriver')

driver.get('https://map.naver.com/')
driver.find_element_by_id('search-input').send_keys('광화문 카페')
driver.find_element_by_css_selector('#header > div.sch > fieldset > button').click()

page = 1
while page < 4:
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	list = soup.select('ul.lst_site > li')
	for data in list:
		detail_url = data.select_one('a.spm_sw_detail').attrs['href']
		time.sleep(1)
		driver2.get('https://map.naver.com'+str(detail_url))
		each = driver2.find_element_by_css_selector(".biz_name_area .name")
		print(each.text)
	page = page + 1
	try:
		driver.find_element_by_xpath('//a[text()=' + str(page) + ']').click()
	except:
		break

driver.close()
driver2.close()

print("\n\n끝")