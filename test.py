#기존 사칙연산외의 수학적 연산을 하기 위해서는 math 모듈 임포팅
import math 

#print(math.ceil(2.451))
#print( 'learning Python'.__len__() )
#print( len('learning Python'))
#print("learning Python")

#print( "eg's tutorial")
# \ 는 이스케이프로 \가 붙으면 문자열들은 특수한 기능을 하게된다
# \" 는 컴퓨터가 이스케이프 뒤의 "을 문자열로 인식한다
#print( "eg's \"tutorial\"")
# \\ 는 이스케이프 뒤에 이스케이프로, 뒤의 이스케이프는 문자열 \로 인식된다
#print( "\\")
# \n = new line 으로 한번 엔터
#print( "eg's\ntutorial")
# \t = new tab 으로 한번 탭
#print( "eg's\ttutorial")
# \a = alerm 으로 컴퓨터에서 알람음
#print( "eg's\atutorial")

## 파이썬은 탭(들여쓰기)를 기준으로 구문들을 그룹핑한다. 
#if True:
#	print("파이썬의 if문의 문법과 실행")
#if False:
#	print("파이썬의 if문의 문법과 실행, False는 실행되지 않는다")

#a = 5
#if a == 3: 
#	print("a는 3이다")
#elif a == 5:
#	print("a는 5이다")
#else:
#	print("a는 3이 아니다")

# input 함수는 기본적으로 다른 코드의 실행을 중지시킨다. 
# 그리고 사용자가 입력한후 엔터를 칠때까지 기다린다.
# 이후 사용자가 엔터 직전까지 입력한 값을 문자열로 반환한다

#in_str = input("id를 입력해주세요!\n")
#id_list = ["pepesi258", "pepesi", "258"]
#print(type(id_list))
#id_1 = "pepesi258"
#id_2 = "pepesi"

#if in_str == id_1 or in_str == id_2:
#	print(in_str.upper()+"님 환영합니다")
#else:
#	print("사용자 접근이 거절되었습니다")

#for 문
#ids = ['a','b','c']
#for n in ids:
#	print(n)

#while 문
#i = 0
#while i<len(ids):
#	print(ids[i])
#	i = i+1

#사용자 지정 함수 만들기, js의 function() 처럼 예약어가 있다.
#예약어: def 
#def myFun():
	#print("사용자 지정함수 실행")
#	return "함수의 리턴 값"
#print(myFun())


## 조건문과 입력자, 사용자 지정함수를 활용해보기
#in_str = input("10미만의 A 반복값을 입력해주세요!\n")
#def FunArgue(num):
#	n = int(num) 
#	if int(n) < 10:
#		print('A'*int(n))
#	else:
#		print('반복값이 너무 큽니다')
#FunArgue(in_str)


####파이썬의 클래스명은 꼭 대문자로 시작해야 한다.
#파이썬의 클래스에서 __init__() 함수는 인스턴스가 선언되면 필수로 실행되는 함수를 가리킨다.
#__init__() 함수의 첫번째 인자를 self로 선언되면 이 self는 생성된 인스턴스 자체를 가리킨다
#파이썬의 self는 js의 this와 비슷하다고 할 수 있음
#class Cal(object):
#	def __init__(self, v1, v2):
		#생성된 인스턴스의 'v1' 속성값은 인자로 넘겨받은 v1
#		self.v1 = v1
#		self.v2 = v2
#	def add(self):
#		return self.v1 + self.v2
#	def substr(self):
#		return self.v1 - self.v2

####인스턴스 생성
#c1 = Cal(10,5)
#오브젝트 인스턴스 c1은 사전에 정의한 __init__ 함수에 의해서 
#v1, v2 속성값을 가지게 된다.
#print( c1.add() )
#print( c1.substr() )
#c2 = Cal(100,30)
#print( c2.add() )
#print( c2.substr() )

# 파이썬의 내장 메소드 isinstace( 인자, 클래스명 ) 는 넘겨받은 첫번째 인자가
# 두번째 인자로 넘겨받은 클래스의 인스턴스가 맞는지를 체크하여 t/f를 리턴한다.
# isinstance( 3, int) 의 경우 3이 정수가 맞는지를 체크한다. 이 경우에는 true 를 리턴한다.

####파이썬의 인스턴의 변수 값을 클래스 밖에서 접근하지 못하게 할 수 있을까? 가능하다.
#class Cal(object):
#	def __init__(self, v1):
#		self.__value = v1
# 이렇게 속성값 앞에 '__' 두개를 붙여주면 클래스 밖에서는 해당 속성값에는 접근할 수가 없다.


###클래스는 상속이 가능하다. 클래스를 선언할때 인자에 상속해주고 싶은 클래스명을 넘겨주면 된다.
#class Class1(object):
#   def method1(self): return 'm1'
#class Class3(Class1):
#    def method2(self): return 'm2'
#c3 = Class3()
#print(c3.method1())



#### 클래스 멤버/메소드
#class Cs:
	#골뱅이는 파이썬에서 사용되는 장식자
	#@staticmethod를 함수위에 붙여주면 아래 함수는 클래스의 static 메소드임을 선언
#	@staticmethod
#    def static_method():
#        print("Static method")
#    @classmethod
#    def class_method(cls):
#        print("Class method")
#    def instance_method(self):
#        print("Instance method")

# 여기서 static method 와 class method 는 클래스의 멤버/소속이다
# 여기서 instance method 는 인스턴스의 멤버/소속이다

#인스턴스 i 생성
#i = Cs()
#Cs.static_method()
#Cs.class_method()
#i.instance_method()


#### 오버라이드 

class C1:
	def m(self):
		return 'parent'
class C2(C1):
	def m(self):
		#return 'child'
		#super()는 부모 클래스
		return super().m() + ' child'
	pass

o = C2()
print(o.m())