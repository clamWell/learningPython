from bs4 import BeautifulSoup  ## str 타입의 text를 html 돔 구조로 변환해주고 쿼리셀렉터, 태그명등으로 접근이 되도록 돕는 모듈
from datetime import datetime ## PC의 시스템 타임 객체를 가져와주는 모듈. currentTime 등.
import requests ## http request 통신 모듈
import pandas as pd ## 파이썬의 리스트, 딕셔너리 타입의 배열을 data table 형태로 변환해주는 모듈


## 데이터타입 타입
listEx = ["기사제목1", "기사제목2", "기사제목3"]
dicEx = {"제목":"기사제목", "날짜":"2020.0724" }


# keywords = input("뉴스 키워드를 입력해주세요!\n")
# print("뉴스를 검색중입니다")

def crawNaverArt():
  rawData = requests.get('https://search.naver.com/search.naver?&where=news&query=박원순 &start=1', headers={'User-Agent': 'Mozilla/5.0'}).text
  html = BeautifulSoup(rawData, 'html.parser')
  newsTitleList = html.select(".news .type01 > li ._sp_each_title")
  # newsTitleList2 = html.findAll("a", class_=" _sp_each_title")

  #print(newsTitleList)

  newsTitle = [];
  newsTitle2 = []

  for news_item in newsTitleList:
    newsTitle.append(news_item.text)

  print(newsTitle)


#crawNaverArt()

def crawNaverArt2():
  rawData = requests.get('https://search.naver.com/search.naver?&where=news&query=박원순 &start=1', headers={'User-Agent': 'Mozilla/5.0'}).text
  html = BeautifulSoup(rawData, 'html.parser')
  news_list = html.select(".news .type01 > li")

  news_dic = [];

  for news_item in news_list:
    title = news_item.select_one("._sp_each_title")
    source = news_item.select_one("._sp_each_source")

    temp = {};
    temp['title'] = title.text
    temp['source'] = source.text.replace("언론사 선정","")
    news_dic.append(temp)
    #print(temp)

  #print(news_dic)
  dataframe = pd.DataFrame(news_dic)
  print(dataframe)

  #now_date = datetime.today().strftime("%Y%m%d%H%M%S")
  outputFileName = "study_craw.xlsx"
  dataframe.to_excel(outputFileName,sheet_name='sheet1',index=False)

crawNaverArt2()
