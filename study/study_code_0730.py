########### 네이버 증권 페이지 긁어오기

from bs4 import BeautifulSoup  ## str 타입의 text를 html 돔 구조로 변환해주고 쿼리셀렉터, 태그명등으로 접근이 되도록 돕는 모듈
from datetime import datetime ## PC의 시스템 타임 객체를 가져와주는 모듈. currentTime 등.
import requests ## http request 통신 모듈
import pandas as pd ## 파이썬의 리스트, 딕셔너리 타입의 배열을 data table 형태로 변환해주는 모듈

def crawNaverFin2():
  rawData = requests.get('https://finance.naver.com/sise/sise_quant_high.nhn', headers={'User-Agent': 'Mozilla/5.0'}).text
  html = BeautifulSoup(rawData, 'html.parser')
  fin_list = html.select(".type_2 tr")

  fin_dic = [];

  for idx, val in enumerate(fin_list):
    check = val.select_one(".tltle")
    #print(check)
    if check:
      title = val.select_one(".tltle")
      fnumber = val.select(".number")

      temp = {};
      temp['증가율'] = fnumber[0].text
      temp['종목명'] = title.text
      temp['현재가'] = fnumber[1].text
      temp['전일비'] = fnumber[2].text
      temp['거래량'] = fnumber[6].text
      temp['전일거래량'] = fnumber[7].text
      temp['PER'] = fnumber[8].text
      fin_dic.append(temp)

  dataframe = pd.DataFrame(fin_dic)
  print(dataframe)

  now_date = datetime.today().strftime("%Y%m%d%H%M%S")
  outputFileName = "study_fincraw.xlsx"
  dataframe.to_excel(outputFileName,sheet_name='sheet1',index=False)

crawNaverFin2()
