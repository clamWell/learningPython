import requests
from bs4 import BeautifulSoup

#### 파이썬을 이용해 가상 브라우저를 조종해보기 ####
from selenium import webdriver
driver = webdriver.Chrome("./chromedriver")

#지금까지의 request와 달리 selenium 라이브러리를 활용한다
#selenium 라이브러리에는 다음과 같은 함수들이 자주 사용된다
#.get() : 해당 url로 이동
#.find_element_by_id() /.find_element_by_class_name(): id/클래스명으로 요소를 찾아 리턴
#.find_element_by_css_selector(): css셀렉터로 요소를 찾아 리턴
# 위 선택자 함수들은 BeautifulSoup 의 select_one()과 유사한 기능을 수행한다
# ~~~.send_keys(): ~~~~ 요소에 인자로 넘겨 받은 값을 입력
# ~~~.click():  ~~~요소를 클릭
# .page_source: 해당 요소의 html 소스를 리턴


#### selenium 이용해 뉴스페이지에 가상브라우저로 접근한다 ####

driver.get("http://www.khan.co.kr/")
driver.find_element_by_id("main_top_search_btn").click()
driver.find_element_by_id("main_top_search_input").send_keys("조국")
driver.find_element_by_id("main_top_search_btn").click()
driver.find_element_by_css_selector(".go_section a").click()

page = 1
while page < 11:
	list = driver.find_elements_by_class_name("phArtc")
	for each_news in list:
		print(each_news.find_element_by_css_selector("dt a").text)
	
	page = page + 1
    #if page % 10 == 1:
    #    driver.find_element_by_class_name('next').click()
    #else:
    #    driver.find_element_by_xpath('//a[text()=' + str(page) + ']').click()
	try:
		driver.find_element_by_class_name('paginate').find_element_by_xpath('//span[text()=' + str(page) + ']').click()
	except: 
		break

driver.close()

print("\n\n끝")

