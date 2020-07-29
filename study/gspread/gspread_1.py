from oauth2client.service_account import ServiceAccountCredentials
##OAuth는 인증을 위한 오픈 스탠더드 프로토콜. 권한 위임, 인증에 대한 표준 방법. 이 패키지의 경우 추측컨대 open authority to client 의 약자인듯. 즉 클라이언트 사용자에게 API 사용/입장 권한을 부여하도록 해주는 라이브러리, 패키지. 이 파이썬 소스코드에서 작성된 요청사항이 목적지인 googleSpreadSheet에 전송되고, 시트를 수정하는 편집 권한의 위임 받기 위해 사용한다.
import gspread
import pandas as pd

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('learn-python-gsrpead-fcd93ccf55bd.json', scope)
gc = gspread.authorize(credentials) ## gspred credentials

#특정 셀의 값을 가져올 수 있다
def getCellValue():
    gc1 = gc.open('learn-python-gsrpead').worksheet('updateDataTest')
    americanoPrice = gc1.acell('C2').value ## 셀이름이나
    lattePrice = gc1.cell(5,3).value ## 행-열 위치로 셀의 값을 가져올 수 있음.

    print("americano Price:")
    print(americanoPrice+"원")
    print("latte Price:")
    print(lattePrice+"원")

#getCellValue()

#특정 열의 값을 가져올 수 있다
def getRowValue():
    gc1 = gc.open('learn-python-gsrpead').worksheet('updateDataTest')
    row1 = gc1.row_values(2)
    row2 = gc1.row_values(3)

    print(row1)
    print(row2)
getRowValue()

#특정 행의 값을 가져올 수 있다
def getColValue():
    gc1 = gc.open('learn-python-gsrpead').worksheet('updateDataTest')
    col1 = gc1.col_values(1)
    col2 = gc1.col_values(2)

    print(col1)
    print(col2)
getColValue()


#.get_all_values()를 이용해 스프레드 시트의 데이터들을 가져온다
def getSheetValue():
    gc1 = gc.open('learn-python-gsrpead').worksheet('openTest')
    # gc1 = gc.open('learn-python-gsrpead')
    # gc1.get_worksheet(0)  > 순서대로 0번째 시트
    # worksheet_list = gc1.worksheets() > 시트리스트 반환
    # new_worksheet = gc1.add_worksheet(title="새로운시트", rows="50", cols="20")
    # gc1.del_worksheet(new_worksheet)

    gc2 = gc1.get_all_values() # 리스트 형태의 값이 리턴

    print(gc2)

#getSheetValue()

# pandas 패키지를 활용해 데이터 프레임 형태로 바꿔줄 수 있다.
def getSheetValueAsDataframe():
    gc1 = gc.open('learn-python-gsrpead').worksheet('updateDataTest')
    gc2 = gc1.get_all_values()
    gc3 = pd.DataFrame(gc2, columns=gc2[0])
    gc3 = gc3.reindex(gc3.index.drop(0))

    print(gc3)

#getSheetValueAsDataframe()

# update_acell() 을 이용해 엑셀 값 업데이트
def updateCell(loc, value):
    gc1 = gc.open('learn-python-gsrpead').worksheet('updateDataTest')
    gc1.update_acell(loc, value)

    sheetValue = gc1.get_all_values()
    sheetValuedf = pd.DataFrame(sheetValue, columns=sheetValue[0])

    print("Menu is...")
    print("===================================")
    print(sheetValuedf)

#updateCell("C2", "3000")


def updateRow():
    gc1 = gc.open('learn-python-gsrpead').worksheet('updateDataTest')
    gc1.update('E1', [[1, 2], [3, 4]]) ## E1 번째 셀을 기준으로 1,2/ 3,4 업데이트

#updateRow()
