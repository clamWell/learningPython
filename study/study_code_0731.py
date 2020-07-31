########### pandas
import pandas as pd ## 파이썬의 리스트, 딕셔너리 타입의 배열을 data table 형태로 변환해주는 모듈
import numpy as np

test_data = {"name":["vue.js", "python", "R", "node.js", "javascript"], "difficulty":[3,2,2,4,3], "studyStage":["start","start","start","before","done"]}
data_df = pd.DataFrame(test_data, columns=["name", "difficulty", "studyStage"])

#연산이 간으한 숫가를 가진 칼럼만 뽑아내고 칼럼에 대한 기본 통계량을 산출해서 알려준다.
print( data_df.describe() )

def colIndexing():
    # 열을 가져온다. 이때 열은 series의 형태로 반한된다.
    print("과목명은?")
    print(data_df["name"]) ## data_df.name 으로도 인덱싱이 가능
    print("---------------------")

    # 두개 이상의 열을 가져온다. 이 경우에는 series가 아닌 데이터프레임 형태로 가져와진다.
    print("과목명과 난이도는?")
    print(data_df[["name","difficulty"]]) ##대괄호가 두개라는 점을 주의한다.
    print("---------------------")

    # 새로운 열 추가
    print("각 과목에 점수를 입력합니다.")
    data_df["score"] = [60, 40, 40, 20, 80] #data_df["score"] = 50 이라고 하게되면 일괄적으로 50 값이 입력된다.
    print(data_df)
    print("---------------------")

    # numpy의 arange() 메소드를 이용한 열 추가
    print("각 과목에 순서를 입력합니다.")
    data_df["randomScore"] = np.arange(5) ## np.arange(n) 은 0부터 n-1까지 1차원 배열을 생성한다는 의미
    print(data_df)
    print("---------------------")

    # series 형태의 데이터로 열 추가
    print("각 과목에 선호도를 입력합니다.")
    tempSe = pd.Series(["like", "soso","love"], index=[0, 2, 4]) ## 이렇게 할때의 장점은 기존의 행 index와 동일한 행으로 알아서 끼어들어간다는 것.
    data_df["prefer"] = tempSe
    print(data_df) ## 대신 값이 없는 행은 NaN이 된다.
    print("---------------------")

    # 조건문으로 t/f의 값으로 데이터 열을 추가
    print("점수에 따라 통과 여부를 입력합니다.")
    data_df["pass"] = data_df["score"] > 50
    print(data_df)
    print("---------------------")

    # del 키워드로 열 삭제하기
    print("필요 없는 열을 정리합니다")
    del data_df["randomScore"]
    print(data_df)
    print("---------------------")

    # 열 목록 조회하기
    print("남아있는 열 목록을 확인합니다.")
    print(data_df.columns)
    print("---------------------")


#colIndexing()

def rowIndexing():
    print("첫번째 과목 정보만 가져옵니다.")
    print(data_df.loc[0]) # .loc[] 함수. index 값을 통해 행을 가져온다.
    print("---------------------")

    print("여러 과목 정보를 가져옵니다.")
    print(data_df.loc[1:3]) # .loc[] 함수. index 값을 통해 행을 가져온다.
    print("---------------------")

    print("첫번째 과목의 난이도 정보만 가져옵니다")
    print(data_df.loc[0, "difficulty"]) # .loc[] 함수는 행을 인덱싱하면서 특정 열의 값만 가져올 수도 있다. 이때 대신 무조건 행의 인덱싱 정보를 먼저 입력한다. 행, 열 순서로.
    print("---------------------")

    print("두번째 과목의 이름, 난이도 정보를 가져옵니다")
    print(data_df.loc[1, ["name","difficulty"]]) # .loc[] 함수는 행을 인덱싱하면서 특정 열의 값만 가져올 수도 있다.
    print("---------------------")

    # 열과 마찬가지의 방법으로 행을 추가할 수 있다.
    print("새로운 과목을 추가합니다.")
    data_df.loc[5] = ["three.js", "4", "start"]
    print(data_df)
    print("---------------------")

    # .iloc() 함수를 사용하면 행과 열의 index 즉 순서값을 토대로 행과 열을 가져올 수 있다.
    print("첫번째부터 세번째 과목의 이름, 난이도 정보를 가져옵니다.")
    print(data_df.iloc[0:3, 0:2]) # data_df.iloc[[0,2,4], [0,3]] 행과 열이 떨어져 있는 경우 원하는 순서값을 리스트 값으로 전달해줄 수 있다.
    print("---------------------")

    print("전체 과목 중 공부가 시작중인 과목은 어떤 과목일까요?")
    test = data_df["studyStage"] == "start"
    print(test) #시리즈 형태로 마스크가 반환됩니다.
    print("---------------------")

    print("전체 과목 중 공부가 시작중인 과목의 이름과 난이도 정보를 가져옵니다.")
    print(data_df.loc[data_df["studyStage"] == "start", ["name","difficulty"]]) # .loc() 함수에 조건문일 입력해 원하는 조건에 부합하는 행만 가져올 수 있습니다.
    print("---------------------")


#rowIndexing()
