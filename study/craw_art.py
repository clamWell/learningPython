#!/usr/bin/env python
# encoding=utf-8

import openpyxl ## 엑셀여는 모듈
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests  ## http request 통신 모듈
import time
from time import sleep ## 차단을 막기 위해 sleep 모듈을 이용해 크롤링 시간차를 준다.
from datetime import datetime
from urllib.request import HTTPError
from os import path
from google.colab import drive

#BOT으로 인한 HTTP 호출 에러인 경우 헤더값 수정을 위해 유저 에이전트 값 몇개 리스트업
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
#Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}

## >> http 통신 유저 에이전트 값을 계속 변경해준다. 이를 통해 네이버 측의 ip 차단을 방지한다.


#구글 드라이브 연동 관련 내용 정의
# notebooks_dir_name = '90.notebook/'
# drive.mount('/content/gdrive')
# notebooks_base_dir = path.join('./gdrive//My Drive/', '90.notebook/')

#!ls './gdrive/My Drive/90.notebook/'
# a = !ls './gdrive/My Drive/

# if not path.exists(notebooks_base_dir):
#   print('Check your google drive directory. See you file explorer')
#   !mkdir './gdrive/My Drive/90.notebook/'

def crawling_test(url, medianame, ref_startpage, ref_endpage):

    page_cnt=1

    try:
      req = requests.get(url, headers = headers)

      #페이지 인코딩방식이 utf-8이 아닌 경우 인코딩 다시 세팅함
      if(req.encoding != 'utf-8'):
        req.encoding = 'utf-8'

      gethtml=req.text
      req.close()

      return find_data(url ,gethtml, medianame, ref_startpage, ref_endpage)

    except HTTPError as e:
      print(e)

#언론사별 최신기사 목록에 섹션명이 표출되지 않는 경우 기사 페이지별로 진입하여 분류명 가져오는 함수(조선일보, 동아일보, 한국일보만 적용됨)
def find_section_to_detail_page(link):
    try:
      req = requests.get(link, headers = headers) #req 인스턴스로 request 통신

      #페이지 인코딩방식이 utf-8이 아닌 경우 인코딩 다시 세팅함
      if(req.encoding != 'utf-8'):
        req.encoding = 'utf-8'

      gethtml=req.text  #응답문의 innerTxt 객체만 가져온다
      req.close() #http 통신 종료
      soup = BeautifulSoup(gethtml, "html.parser") #str로 나열되어 있는 응답문 innerTxt을 html 구조로 변경해준다.
      sleep(2)

      if 'chosun' in link:
          section = soup.find('head').find('meta',{'property':'article:section'}).get('content')

      elif 'donga' in link:
          if 'dobal' in link: #기본 기사 페이지 형식 외 다른 기사페이지 양식이 존재하여 해당 기사인 경우 예외처리함
            section = '오피니언 추정'
          elif 'sports' in link:#스포츠 동아 페이지인 경우
            section = soup.find('head').find('meta',{'name':'categoryname'}).get('content')
          else:
            section = soup.find('head').find('meta',{'name':'categoryname'}).get('content')

      elif 'hankookilbo' in link:
          section = soup.find('head').find('meta',{'property':'article:section'}).get('content')

      else: #가져오지 못하는 경우 section명 예외 처리
          section = 'Null'

      return section

    except HTTPError as e:
      print(e)
      section = 'Null'
      print('HTTPError로 아래에 URL에서 Section명을 수집할 수 없습니다.')
      print(link)
      return section

#언론사별 최신기사 목록을 리스트(배열)형태로 저장하는 함수)
#베이스링크인 url, req 통신 응답으로 받은 innertxt, 매체명, 시작, 끝 페이지를 인자로 넘겨받는다.
def find_data(url, gethtml, medianame, ref_startpage, ref_endpage):
    soup = BeautifulSoup(gethtml, "html.parser")

    if medianame == 'chosun':
        list = soup.find_all('dl','list_item')

    elif medianame == 'joins':
        list = soup.find('div','mg list').find_all('li')

    elif medianame == 'donga':
        list = soup.find_all('div','articleList')

    elif medianame == 'hani':
        list = soup.find('div','section-list-area ').find_all('div','list')

    elif medianame == 'hankook':
        list = soup.find('div','wrap').find_all('div', {'class':'inn'}) ## .inn 클래스로 셀렉팅을 하자 최상단 네비도 같이 수집이 되어버린다.

        del_cnt=0
        for item in list: ## 수집한 배열 list를 for in을 통해 검토한다
          if 'toast-last-read-a-tag' in str(item): ## 최상단 네비에는 toast-last-read-a-tag 를 id로 가진 a링크가 들어있다. 이를 체크해서 만약 이 조건에 해당한다면
            del list[del_cnt] # 해당 요소는 배열에서 삭제한다.
          del_cnt=del_cnt+1

    #print(list)

        # list.extend(list_appned)

    #print(list)
    i=0
    #
    return_number=1
    count=1
    today_time=datetime.today().strftime("%Y%m%d%H%M%S")
    # filepath = notebooks_base_dir
    filename = medianame+'_'+str(ref_startpage)+'page_to_'+str(ref_endpage)+'page_'+today_time+'.txt'
    f = open(filename,'a',encoding='utf-8')
    # print(notebooks_base_dir, '구글드라이브 폴더에 텍스트 파일을 자동 생성하였습니다.')

    for item in list:
        if item.find('a') is None:
            print(medianame, "언론사의 목록에서 정보를 찾을 수 없습니다. 다음 목록으로 다시 시도합니다.")
            continue


        link = item.find('a')['href']

        section ='default'

        if medianame == 'chosun':
            title = item.find('dt').find('a').text
            title = re.sub('\n','',title)
            link = "https:"+link
            section = find_section_to_detail_page(link)
            date = item.find('span', 'date').text
            #sheet1.append([date, section, title, link])


        elif medianame == 'joins':
            title = item.find('strong').text
            title = re.sub('\n','',title)
            link = "https://news.joins.com"+link
            temp_title = title
            title = re.sub(' \|.*','',title)
            section = re.sub('.* \| ','',temp_title)
            date = re.sub('https://news.joins.com/sitemap/index/','',url)
            #sheet2.append([date, section, title, link])

        elif medianame == 'donga':
            if 'error_page' in soup.find('div', {'id':'container'}):
              print('오류 페이지입니다. (삭제된 기사로 추정됨)')
              print(link)
              continue
            else:
              title = item.find('span', class_='tit').text #동아일보
              title = re.sub('\n','',title)
              date = item.find('span', class_='date').text #동아일보
              section = find_section_to_detail_page(link)
              input_to_text=str(date)+' ; '+str(section)+' ; '+str(title)+' ; '+str(link)
              f.write(input_to_text)
              f.write('\n')

        elif medianame == 'hani':
            title = item.find('h4','article-title').text
            title = re.sub('\n','',title)
            link = "http://www.hani.co.kr"+link
            section = item.find('strong','category').text
            section = re.sub('\n','',section)
            date = item.find('span', {'class':'date'}).text
            # if  ENDDATE_1 in date:
            #     return_number=0
            #     break

        elif medianame == 'hankook':
            #검색페이지 1페이지 인경우 목록 요소중 첫번째에 대해서 별도 예외 처리하지 못함. 따라서 스크래핑과 별도로 수기 입력하여 추가해야 함
            if 'h2' in str(item): #h2인경우(검색페이지의 1페이지인 경우) 목록 요소에 작성일이 있기 때문에 default로 표시하되 수집 후  따라서 스크래핑과 별도로 수기 수정입력 해야함
              title = item.find('h2').find('a').text
              title = re.sub('\n','',title)
              link = item.find('h2').find('a')['href']
              date = "1945.08.15"
            elif 'h3' in str(item):
              title = item.find('h3').find('a').text
              title = re.sub('\n','',title)
              link = item.find('h3').find('a')['href']
              date = item.find('p', {'class':'date'}).text
              date = re.sub('\n','',date)
              date = re.sub('&nbsp;','',date)

            else:
              title = str(i+1)+'번째 확인 필요함'
              link = 'https://www.hankookilbo.com/'
              date = str(i+1)+'번째 확인 필요함'
              print(item)

            link="https://www.hankookilbo.com/"+link
            section = find_section_to_detail_page(link)
            date = re.sub('&nbsp;','',date)

        input_to_text=str(date)+' ; '+str(section)+' ; '+str(title)+' ; '+str(link)
        f.write(input_to_text)
        f.write('\n')

        print(date,',' ,section, ',',title, ',',link)

        i=i+1
        sleep(3)
    f.close()
    print(filename, " 텍스트 파일을 구글 드라이브에 저장하였습니다.")
    return return_number
# wb = openpyxl.load_workbook('thepress_article.xlsx')
# sheet1 = wb['조선일보']
# sheet2 = wb['중앙일보']
# sheet3 = wb['동아일보']
# sheet4 = wb['한겨레']
# sheet5 = wb['한국일보']
# sheet6 = wb['경향신문']

#스크래핑할 언론사별 URL 목록 정의
URL_SHEET1 ='https://news.chosun.com/svc/list_in/list.html?pn='
URL_SHEET4 ='http://www.hani.co.kr/arti/list'
URL_SHEET5 ='https://www.hankookilbo.com/Search?Page='
URL_SHEET5_query = '&tab=NEWS&sort=recent&searchText=&searchTypeSet=TITLE,CONTENTS&realPaperYN=false&startDate=2020-05-01%2000:00:00&endDate=2020-05-31%2000:00:00&selectedPeriod=manual&sections=SOCIETY,ECONOMY,OPINION,WORLD,ENTER,POLITICS,CULTURE,SPORTS,LOCAL,FOCUS'



def crawling_media(ref_media_name, ref_base_url, ref_startdate, ref_enddate, ref_startpage, ref_endpage):
  MEDIA_NAME = ref_media_name
  BASE_URL = ref_base_url
  START_DATE = ref_startdate
  END_DATE = ref_enddate
  START_PAGE = ref_startpage
  END_PAGE = ref_endpage
  #print(type(START_PAGE))
  return_number=1

  if 'hankook' in MEDIA_NAME:
    URL_SEARCH_QUERY='&tab=NEWS&sort=relation&searchText=&searchTypeSet=TITLE,CONTENTS&realPaperYN=false&startDate='+START_DATE+'%2000:00:00&endDate='+END_DATE+'%2000:00:00&selectedPeriod=manual&sections=SOCIETY,ECONOMY,OPINION,WORLD,ENTER,POLITICS,CULTURE,SPORTS,LOCAL,FOCUS'

  while return_number > 0:
    if 'chosun' in MEDIA_NAME:
      URL = BASE_URL+str(START_PAGE)
    elif 'joins' in MEDIA_NAME:
      if START_PAGE <10:
        URL =BASE_URL+'0'+str(START_PAGE)
      else:
        URL = BASE_URL+str(START_PAGE)

    elif 'donga' in MEDIA_NAME:
      URL = BASE_URL+str(START_PAGE)

    elif 'hani' in MEDIA_NAME:
      URL = BASE_URL+str(START_PAGE)+'.html'
    elif 'hankook' in MEDIA_NAME:
      URL = BASE_URL+str(START_PAGE)+URL_SEARCH_QUERY

    return_number= crawling_test(URL, MEDIA_NAME,START_PAGE, END_PAGE)
    print(START_PAGE, "페이지가 완료되었습니다.")

    if 'donga' in MEDIA_NAME:
      START_PAGE = START_PAGE+20
    else:
      START_PAGE = START_PAGE+1

    if START_PAGE > END_PAGE:
        break
    #wb.save('thepress_article.xlsx')
    #print("엑셀파일을 저장 완료하였습니다.")
    sleep(3)




def input_data_step01():
  print("Step01")
  print("1. 조선일보")
  print("2. 중앙일보")
  print("3. 동아일보")
  print("4. 한겨레")
  print("5. 한국일보")
  print("===================================================")
  print("0. 종료하기")
  input_media = input("상단 목록에서 스크래핑할 언론사의 숫자를 입력하세요. \n")

  if input_media =='1' or input_media =='2' or input_media =='3' or input_media =='4' or input_media =='5':
    input_data_step02(input_media) #Step02 함수 호출

  elif input_media =='0':
    return 0

  else:
    print("잘못입력하셨습니다. 처음으로 돌아갑니다. \n")
    input_data_step01()

def input_data_step02(input_media):

  if input_media == '1':
    medianame = 'chosun'

    print("조선일보의 최신기사 목록에서 데이터를 수집하겠습니다.")
    print("https://news.chosun.com/svc/list_in/list.html")
    print("Step02")
    print("1. 전체 기사 목록(스포츠 조선, 뉴시스, 연합 등 포함")
    print("2. 조선일보 기사만")
    print("===================================================")
    print("9. 언론사 선택으로 돌아가기(처음으로)")
    print("0. 종료하기")
    chosun_article_sort = input("상단 목록에서 수집할 기사의 종류를 선택하세요. \n")
    if chosun_article_sort == '1':
      print('1번을 선택하였습니다.')
      BASE_URL='https://news.chosun.com/svc/list_in/list.html?pn='
      START_INPUT = int(input("시작 페이지 정보 입력\n"))
      END_INPUT = int(input("종료 페이지 정보 입력\n"))
      crawling_media(medianame, BASE_URL, 'null', 'null', START_INPUT, END_INPUT)
    elif chosun_article_sort == '2':
      print('2번을 선택하였습니다.')
      BASE_URL='https://news.chosun.com/svc/list_in/list.html?source=1&pn='
      START_INPUT = int(input("시작 페이지 정보 입력\n"))
      END_INPUT = int(input("종료 페이지 정보 입력\n"))
      crawling_media(medianame, BASE_URL, 'null', 'null', START_INPUT, END_INPUT)

    elif chosun_article_sort == '9':
      input_data_step01()
    elif chosun_article_sort == '0':
      return 0


  elif input_media == '2':
    medianame = 'joins'

    print("중앙일보의 최신기사 목록에서 데이터를 수집하겠습니다.")
    print("https://news.joins.com/sitemap/index/")
    print("Step02")
    print("===================================================")
    print("언론사 선택으로 돌아가기(처음으로): HOME")
    print("종료하기: EXIT")
    print("상단의 매칭되는 영문을 입력하여 이전단계로 돌아가거나, 수집할 기사의 날짜 정보를 입력하세요. 중앙일보는 같은 연도와 월을 기준으로 시작일과 종료일을 설정합니다.")
    YEAR_INPUT = input("연도 정보 입력(4자리 숫자)\n")
    MONTH_INPUT = input("월 정보 입력(2자리 숫자)\n")
    START_INPUT = int(input("시작일 입력(2자리 숫자)\n"))
    END_INPUT = int(input("종료일 입력(2자리 숫자)\n"))
    BASE_URL='https://news.joins.com/sitemap/index/' + str(YEAR_INPUT) + '/'+ str(MONTH_INPUT) + '/'

    if YEAR_INPUT == 'HOME' or MONTH_INPUT == 'HOME' or START_INPUT == 'HOME' or END_INPUT == 'HOME':
      input_data_step01()
    elif YEAR_INPUT == 'EXIT' or MONTH_INPUT == 'EXIT' or START_INPUT == 'EXIT' or END_INPUT == 'EXIT':
      return 0
    crawling_media(medianame, BASE_URL, 'null', 'null', START_INPUT, END_INPUT)


  elif input_media == '3':
    medianame = 'donga'

    print("동아일보의 최신기사 목록에서 데이터를 수집하겠습니다.")
    print("https://www.donga.com/news/List?p=1")
    print("Step02")
    print("===================================================")
    print("언론사 선택으로 돌아가기(처음으로): HOME")
    print("종료하기: EXIT")
    print("상단의 매칭되는 영문을 입력하여 이전단계로 돌아가거나, 수집할 기사의 시작페이지와 종료페이지 정보를 입력하세요.")
    print("동아일보는 페이지 번호가 아닌, 상단 URL 주소에서 List?p= 다음의 숫자 정보를 입력하세요.")
    START_INPUT = int(input("시작 페이지 정보 입력\n"))
    END_INPUT = int(input("종료 페이지 정보 입력\n"))
    BASE_URL='https://www.donga.com/news/List?p='

    if START_INPUT == 'HOME' or END_INPUT == 'HOME':
      input_data_step01()
    elif START_INPUT == 'EXIT' or END_INPUT == 'EXIT':
      return 0
    crawling_media(medianame, BASE_URL, 'null', 'null', START_INPUT, END_INPUT)

  elif input_media == '4':
    medianame = 'hani'

    print("한겨레의 최신기사 목록에서 데이터를 수집하겠습니다.")
    print("http://www.hani.co.kr/arti/list1.html")
    print("Step02")
    print("===================================================")
    print("언론사 선택으로 돌아가기(처음으로): HOME")
    print("종료하기: EXIT")
    print("상단의 매칭되는 영문을 입력하여 이전단계로 돌아가거나, 수집할 기사의 시작페이지 번호와 종료페이지 번호를 입력하세요.")
    START_INPUT = int(input("시작 페이지 번호 입력\n"))
    END_INPUT = int(input("종료 페이지 번호 입력\n"))
    BASE_URL='http://www.hani.co.kr/arti/list'

    if START_INPUT == 'HOME' or END_INPUT == 'HOME':
      input_data_step01()
    elif START_INPUT == 'EXIT' or END_INPUT == 'EXIT':
      return 0

    crawling_media(medianame, BASE_URL, 'null', 'null', START_INPUT, END_INPUT)

  elif input_media == '5':
    medianame = 'hankook'

    print("한국일보의 최신기사 목록에서 데이터를 수집하겠습니다.")
    print("https://www.hankookilbo.com/Search")
    print("Step02")
    print("===================================================")
    print("언론사 선택으로 돌아가기(처음으로): HOME")
    print("종료하기: EXIT")
    print("상단의 매칭되는 영문을 입력하여 이전단계로 돌아가거나, 수집할 기사의 정보를 입력하세요.")
    STARTDATE_HANKOOK = input("검색 시작일 입력(ex. 2020-06-01 과 같이 - 기호 사용)\n")
    ENDDATE_HANKOOK = input("검색 종료일 입력(ex. 2020-06-01 과 같이 - 기호 사용)\n")
    Default_URL = "https://www.hankookilbo.com/Search?Page=1&tab=NEWS&sort=relation&searchText=&searchTypeSet=TITLE,CONTENTS&realPaperYN=false&startDate="+STARTDATE_HANKOOK+"%2000:00:00&endDate="+ENDDATE_HANKOOK+"%2000:00:00&selectedPeriod=manual&sections=SOCIETY,ECONOMY,OPINION,WORLD,ENTER,POLITICS,CULTURE,SPORTS,LOCAL,FOCUS"
    print("상단 URL 정보에서 수집할 시작페이지 번호와 종료 페이지 번호를 입력하세요.")
    START_INPUT = int(input("시작 페이지 정보 입력\n"))
    END_INPUT = int(input("종료 페이지 정보 입력\n"))

    BASE_URL='https://www.hankookilbo.com/Search?Page='
    if STARTDATE_HANKOOK == 'HOME' or ENDDATE_HANKOOK == 'HOME' or START_INPUT == 'HOME' or END_INPUT == 'HOME':
      input_data_step01()
    elif START_INPUT == 'EXIT' or END_INPUT == 'EXIT' or START_INPUT == 'EXIT' or END_INPUT == 'EXIT':
      return 0

    crawling_media(medianame, BASE_URL, STARTDATE_HANKOOK, ENDDATE_HANKOOK, START_INPUT, END_INPUT)




#####하단 입력 표출 및 언론사와 페이지 범위 입력받도록 하는 영역#####
input_data_step01()
print("종료되었습니다.")
