#======================================================================
# 작성자 : 류병선
# 
# 기능 : 각 지역별 감염병'쯔쯔가무시'의 위험수치를 예측하여 지도에 시각화하는 UI
#=======================================================================

from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

import 데이터관리함수 as dmf
import 그래프함수 as gmf
import folium

import matplotlib.pyplot as plt
from matplotlib import style
import random as rd

from tkinter import *
from tkinter import ttk
import easygui as eg

#<Main>===========================================================================

# --------------------------------------------------------------------------------
# Global 변수 설정 및 옵션
# --------------------------------------------------------------------------------

파일이름 = ''
출력파일이름 = ''
지역리스트 =['강원도','경기도','대전광역시','대구광역시','울산광역시','부산광역시','광주광역시','경상북도','경상남도','전라북도','전라남도','충청남도','충청북도','인천광역시']
속성리스트 = []
속성리스트1 = []
데이터리스트 = []
속성사전 = {}
선택속성 = []
선택속성색인 = []
리스트 =[]
출력리스트 = []
입력구분자 = ','
출력구분자 = ','
빈크기 = 10
목적속성 = ''
# --------------------------------------------------------------------------------
# 창 생성
# --------------------------------------------------------------------------------

창 = Tk()
창.title('Data Analysis User interface')
창.config(width=1164, height=768, bg='gray')

# --------------------------------------------------------------------------------
# 파일 매뉴 화면 구성
# --------------------------------------------------------------------------------
# File Menu Frame 생성
파일메뉴화면 = ttk.Frame(창, padding=(5, 5))
파일메뉴화면.place(height=82, width=1170, x=2, y=2) 

# 파일 레이블 
파일레이블 = ttk.Label(파일메뉴화면, text='파일관리', width=20)
파일레이블.grid(row=0, sticky=W)

# 출력 리스트 생성
def 이중리스트출력(이중리스트):
    데이터보기.delete('1.0',END)
    for line in 이중리스트:
        문자열 = ''
        for each in line:
            문자열 = 문자열 + each + '\t' + '\t'
        데이터보기.insert('end', 문자열 + '\n')

# 선택 속성 리스트에 속성 추가
def 속성리스트_생성(속성):
    크기 = len(데이터리스트)
    리스트=[]
    지역리스트=[]
    색인=dmf.속성색인찾기(속성리스트,'시도')
    for i in range(0,크기):
        리스트.append(데이터리스트[i][색인])
    지역리스트=set(리스트)
    속성리스트박스.delete(0, 'end')
    for each in 지역리스트:
        속성리스트박스.insert('end', each)

# 파일 오픈 버튼
def 파일선택():
    global 파일이름, 입력구분자, 속성리스트, 데이터리스트, 속성사전, 출력리스트, 선택속성, 빈크기, 목적속성
    파일이름 = ''
    입력구분자 = 입력구분자입력공간.get()
    속성리스트 = []
    데이터리스트 = []
    속성사전 = {}
    출력리스트 = []
    선택속성 = []
    빈크기 = 10
    목적속성 = ''
    파일이름입력공간.delete(0,'end')
    데이터보기.delete('1.0', END)

    파일이름 = eg.fileopenbox(msg='파일열기', title='파일열기', default='*', filetypes=None, multiple=False)
    if 파일이름 == None: eg.msgbox('파일이 선택되지 않았습니다.', title='오류')
    else: 
        파일이름입력공간.insert(0, 파일이름)
        속성리스트, 데이터리스트 = dmf.테이블_생성(파일이름, 입력구분자)
        속성사전 = dmf.속성사전_생성(속성리스트, 데이터리스트)
        선택속성 = 속성리스트.copy()
        속성리스트_생성(속성리스트)

파일열기 = ttk.Button(파일메뉴화면, text='파일불러오기', width=18, command=파일선택)
파일열기.grid(row=1, sticky=(W,N))

# 파일 저장 버튼
def file_save():
    global 출력파일이름, 출력구분자, 속성리스트, 데이터리스트, 속성사전, 출력리스트, 선택속성, 빈크기, 목적속성
    출력파일이름 = 출력파일이름입력공간.get()
    출력구분자 = 출력구분자입력공간.get()
    if 출력파일이름 == '': eg.msgbox('저장할 파일명을 입력해주세요.', title='오류')
    else :
        in_split = 파일이름.split('\\')
        out_split = 출력파일이름.split('\\')
        if in_split[-1] == out_split[-1]: eg.msgbox('원본 파일과 다른 이름으로 입력해주세요.', title='오류')
        else:
            print(out_split)
            dmf.데이터파일출력(출력파일이름, 출력리스트, 출력구분자) # 출력 데이터 리스트명을 수정해야 함

파일저장 = ttk.Button(파일메뉴화면, text='파일저장하기', width=18, command=file_save)
파일저장.grid(row=2, sticky=(W,N))

# --------------------------------------------------------------------------------
# 파일 상태 화면 구성
# --------------------------------------------------------------------------------
# File 상태 frame 생성

파일상태화면 = ttk.Frame(창, padding=(5, 5))
파일상태화면.place(height=82, width=868, x=154, y=2) 
ttk.Label(파일상태화면, width=10).grid(column=0, row=0, sticky=W) # 공백출력

# 불러온 파일 위치 레이블
파일역할레이블 = ttk.Label(파일상태화면, text='불러온 파일 위치', width=14)
파일역할레이블.grid(column=0, row=1, sticky=(W,N))

# 파일 명 입력 공간
파일이름입력공간 = ttk.Entry(파일상태화면, width=70, textvariable=파일이름)
파일이름입력공간.grid(column=1, row=1)

# 입력 구분자 레이블
ttk.Label(파일상태화면, width=2).grid(column=2, row=1, sticky=W) # 공백출력
입력구분자레이블 = ttk.Label(파일상태화면, text='입력 구분자', width=10)
입력구분자레이블.grid(column=3, row=1, sticky=W)

# 입력 구분자 입력 공간
입력파일구분자 = StringVar()
입력구분자입력공간 = ttk.Entry(파일상태화면, width=5, textvariable=입력파일구분자, justify='center')
입력구분자입력공간.insert(0, 입력구분자)
입력구분자입력공간.grid(column=4, row=1, sticky=(W,N))

# 구분자 적용 버튼
def 입력구분자적용():
    global 입력구분자
    입력구분자 = 입력구분자입력공간.get()
    #print(입력구분자)
    if '\\t' in 입력구분자: 입력구분자 = '\t'; 입력구분자입력공간
    elif '\\n' in 입력구분자: 입력구분자 = '\n'

ttk.Label(파일상태화면, width=1).grid(column=5, row=1, sticky=W) # 공백출력
입력구분자적용버튼 = ttk.Button(파일상태화면, text='입력 구분자 적용', width=14, command=입력구분자적용)
입력구분자적용버튼.grid(column=6, row=1, sticky=(W,N))

# 저장 파일 이름 레이블

파일역할레이블 = ttk.Label(파일상태화면, text='저장 파일 이름', width=14)
파일역할레이블.grid(column=0, row=2, sticky=(W,N))

# 출력 파일 명 입력 공간

출력파일이름입력공간 = ttk.Entry(파일상태화면, width=70, textvariable=출력파일이름)
출력파일이름입력공간.grid(column=1, row=2)

# 출력 구분자 레이블

출력구분자레이블 = ttk.Label(파일상태화면, text='출력 구분자', width=10)
출력구분자레이블.grid(column=3, row=2, sticky=W)

# 출력 구분자 입력 공간

출력파일구분자 = StringVar()
출력구분자입력공간 = ttk.Entry(파일상태화면, width=5, textvariable=출력파일구분자, justify='center')
출력구분자입력공간.insert(0, 출력구분자)
출력구분자입력공간.grid(column=4, row=2, sticky=(W,N))

# 구분자 적용 버튼

def 출력구분자적용():
    global 출력구분자
    출력구분자 = 출력구분자입력공간.get()
    #print(출력구분자)
    if '\\t' in 출력구분자:
        출력구분자 = '\t'
        출력구분자입력공간
    elif '\\n' in 출력구분자:
        출력구분자 = '\n'

ttk.Label(파일상태화면, width=1).grid(column=5, row=2, sticky=W) # 공백출력
출력구분자적용버튼 = ttk.Button(파일상태화면, text='출력 구분자 적용', width=14, command=출력구분자적용)
출력구분자적용버튼.grid(column=6, row=2, sticky=(W,N))

# --------------------------------------------------------------------------------
# 시군구  목록 Frame 구성
# --------------------------------------------------------------------------------
# 여분 frame 생성

속성화면 = ttk.Frame(창, padding=(5, 5))
속성화면.place(height=680, width=150, x=2, y=86)

속성화면2 = ttk.Frame(창, padding=(5, 5))
속성화면2.place(height=680, width=150, x=154, y=86)

속성레이블 = ttk.Label(속성화면, text='시/도 목록', width=13)
속성레이블.grid(column=0, row=0, sticky=W)

# 속성 목록 레이블

속성레이블1 = ttk.Label(속성화면2, text='시/군/구 목록', width=13)
속성레이블1.grid(column=0, row=0, sticky=W)

# 지역속성 적용 버튼
 
def 지역속성적용하기():
    global 속성리스트, 데이터리스트, 출력리스트, 선택속성, 선택속성색인
    크기 = len(데이터리스트)
    출력리스트 = []; 선택속성 = []; 선택속성색인 = []
    선택속성 = 속성리스트박스.selection_get().strip().split('\n')
    i = 0
    j = 0
    count =len(선택속성)
    색인 =dmf.속성색인찾기(속성리스트,'시군구')
    속성리스트박스1.delete(0, 'end')
    while j <count:
        i=0
        while i < 크기:
            if 선택속성[j]==데이터리스트[i][0]:
                출력리스트.append(데이터리스트[i][색인])

            i=i+1
        j=j+1
    for each in 출력리스트:
        속성리스트박스1.insert('end',each)
        
def 세부지역적용하기():#수정
    global 속성리스트,데이터리스트, 출력리스트, 선택속성, 선택속성색인
    출력리스트 = []
    선택시군구속성=[]
    리스트 =[]
    크기 = len(데이터리스트)
    선택시군구속성 = 속성리스트박스1.selection_get().strip().split('\n')
    선택속성 = ['시도','시군구','위험지수','농가여자_P1','답_P0','대지_P0','남자인구_P1','기온_9월20이상','농가여자_P2','기온_7월25이상','전_P0','과수원_P0']
    선택속성색인 = []
    색인 =dmf.속성색인찾기(속성리스트,'시군구')
    for each in 선택속성: 선택속성색인.append(속성리스트.index(each))
    i = 0
    while i < 크기:
        buf = []
        for each_i in 선택속성색인:
            buf.append(데이터리스트[i][each_i])
            출력리스트.append(buf)
        i = i + 1
    출력리스트.insert(0,선택속성)
    크기크기 = len(선택시군구속성)
    크기출력= len(출력리스트)
    k =0
    while k < 크기크기:
        x = 1
        while x < 크기출력:
            if 출력리스트[x][1] == 선택시군구속성[k]:
                리스트.append(출력리스트[x])
            x= x+1
        k=k+1
    리스트.insert(0,선택속성)
    이중리스트출력(리스트)



속성적용버튼 = ttk.Button(속성화면, text='시/도 선택적용', width=16, command=지역속성적용하기)
속성적용버튼.grid(column=0, row=1, sticky=E)

속성적용버튼1 = ttk.Button(속성화면2, text='시/군/구 선택적용', width=16, command=세부지역적용하기)
속성적용버튼1.grid(column=0, row=1, sticky=E)

# 속성 목록 리스트 박스
속성리스트박스 = Listbox(속성화면, height=35, width=16, selectmode=MULTIPLE)
속성리스트박스.grid(column=0, row=2, sticky=(N,W,E,S))

속성리스트박스1 = Listbox(속성화면2, height=35, width=16, selectmode=MULTIPLE)
속성리스트박스1.grid(column=0, row=2, sticky=(N,W,E,S))

# 속성 목록 리스트 박스 스크롤

속성목록스크롤 = ttk.Scrollbar(속성화면, orient=VERTICAL, command=속성리스트박스.yview)
속성목록스크롤.grid(column=1, row=2, sticky=(N,S))
속성리스트박스['yscrollcommand'] = 속성목록스크롤.set
속성리스트박스.insert(0, '#없음#')


속성목록스크롤1 = ttk.Scrollbar(속성화면2, orient=VERTICAL, command=속성리스트박스1.yview)
속성목록스크롤1.grid(column=1, row=2, sticky=(N,S))
속성리스트박스1['yscrollcommand'] = 속성목록스크롤1.set
속성리스트박스1.insert(0, '#없음#')


# 속성 전체 선택 버튼

def 모든속성선택하기():
    속성리스트박스.selection_set(0, 'end')

def 모든속성선택하기1():
    속성리스트박스1.selection_set(0, 'end')

속성전체선택버튼 = ttk.Button(속성화면, text='속성 전체 선택', width=16, command=모든속성선택하기)
속성전체선택버튼.grid(column=0, row=3, sticky=E)

속성전체선택버튼1 = ttk.Button(속성화면2, text='속성 전체 선택', width=16, command=모든속성선택하기1)
속성전체선택버튼1.grid(column=0, row=3, sticky=E)

# 모든 속성 해제 버튼

def 모든속성해제하기():
    속성리스트박스.selection_clear(0, 'end')

def 모든속성해제하기1():
    속성리스트박스1.selection_clear(0, 'end')

속성전체해제버튼 = ttk.Button(속성화면, text='속성 전체 해제', width=16, command=모든속성해제하기)
속성전체해제버튼.grid(column=0, row=4, sticky=E)

속성전체해제버튼1 = ttk.Button(속성화면2, text='속성 전체 해제', width=16, command=모든속성해제하기1)
속성전체해제버튼1.grid(column=0, row=4, sticky=E)


# --------------------------------------------------------------------------------
# 데이터 분석 Frame 구성
# --------------------------------------------------------------------------------

# 데이터 분석 Frame 구성
데이터분석기능=ttk.Frame(창,padding=(5,5))
데이터분석기능.place(height=40,width=868,x=306,y=86)

# 데이터 분석 레이블
데이터분석레이블=ttk.Label(데이터분석기능,text='데이터 분석 기능', width=20).grid(column=0, row=1, sticky=W)

# 데이터 분석 버튼 1
def CART분석():
    크기 = len(데이터리스트)
    i=0
    선택속성 = ['시도','시군구','위험지수','농가여자_P1','답_P0','대지_P0','남자인구_P1','기온_9월20이상','농가여자_P2','기온_7월25이상','전_P0','과수원_P0']
    while i < 크기:
        if(float(데이터리스트[i][3])>13.856):
            if(float(데이터리스트[i][6])>48.744):
                if(float(데이터리스트[i][4])<=5.044):
                    데이터리스트[i][2] =str(6.455)
                    
                else:
                    if(float(데이터리스트[i][11])<=0.720):
                        if(float(데이터리스트[i][10])<=6.833):
                            데이터리스트[i][2] =str(136.667)
                            
                        else:
                            데이터리스트[i][2] =str(75.933)
                            
                    else:
                        데이터리스트[i][2] =str(32.167) 
            else:
                데이터리스트[i][2] =str(147.029)
                
        else:
            if(float(데이터리스트[i][4])>8.831):
                if(float(데이터리스트[i][5])<=3.133):
                    if(float(데이터리스트[i][3]) <=3.438):
                        if(float(데이터리스트[i][10])<=6.041):
                            데이터리스트[i][2] =str(21.8)
                        else:
                            데이터리스트[i][2] =str(4.778)
                            
                    else:
                        데이터리스트[i][2] =str(26.741)
                        
                else:
                    if(float(데이터리스트[i][7])<=443):
                        if(float(데이터리스트[i][8])<=50.641):
                            데이터리스트[i][2] =str(15.4)
                        else:
                            데이터리스트[i][2] =str(48.211)
                            
                    else:
                        데이터리스트[i][2] =str(90.0)
                        
            else:
                if(float(데이터리스트[i][5])>65.765):
                    데이터리스트[i][2] =str(49.286)
                else:
                    if(float(데이터리스트[i][5]<=23.548)):
                       데이터리스트[i][2] =str(6.081)
                       
                    else:
                       if(float(데이터리스트[i][9]<=547)):
                          데이터리스트[i][2] =str(14.593)
                          
                       else:
                          데이터리스트[i][2] =str(29.5)
        i=i+1
    데이터리스트.insert(0,선택속성)
    이중리스트출력(데이터리스트)

        
데이터분석버튼1= ttk.Button(데이터분석기능,text='CART분석',width=18,command=CART분석)
데이터분석버튼1.grid(column=1,row=1,sticky=W)

# 데이터 분석 버튼 2
def 지도내보내기():
    map_osm = folium.Map()
    global 속성리스트,데이터리스트, 출력리스트, 선택속성, 선택속성색인,리스트
    선택시군구속성=[]
    크기 = len(데이터리스트)
    선택시군구속성 = 속성리스트박스1.selection_get().strip().split('\n')
    선택속성 = ['시도','시군구','위도','경도','color']
    선택속성색인 = []
    색인 =dmf.속성색인찾기(속성리스트,'시군구')
    for each in 선택속성:
        선택속성색인.append(속성리스트.index(each))
    i = 0
    while i < 크기:
        buf = []
        for each_i in 선택속성색인:
            buf.append(데이터리스트[i][each_i])
            출력리스트.append(buf)
        i = i + 1
    출력리스트.insert(0,선택속성)
    크기크기 = len(선택시군구속성)
    크기출력= len(출력리스트)
    k =0
    folium.Map(location=[35.2048575,129.0836402])
    while k < 크기크기:
        x = 1
        while x < 크기출력:
            if 출력리스트[x][1] == 선택시군구속성[k]:
                folium.Marker([float(출력리스트[x][2]),float(출력리스트[x][3])], popup=선택시군구속성[k], icon=folium.Icon(color=str(출력리스트[x][4]),icon='cloud')).add_to(map_osm)
            x = x+1
        k=k+1
    map_osm.save(outfile='map.html')

데이터분석버튼2= ttk.Button(데이터분석기능,text='지도 내보내기',width=18,command=지도내보내기)
데이터분석버튼2.grid(column=2,row=1,sticky=W)


# --------------------------------------------------------------------------------
# 데이터 결과 Frame 구성
# --------------------------------------------------------------------------------
# 데이터 결과 Frame 생성
데이터결과화면 = ttk.Frame(창, padding=(5, 5))
데이터결과화면.place(height=638, width=858, x=306, y=128) 

# 데이터 결과 레이블
데이터결과레이블 = ttk.Label(데이터결과화면, text='데이터 화면', width=20).grid(column=0, row=0, sticky=W)

# 데이터 표현 공간 : 리스트 박스
데이터보기 = Text(데이터결과화면, height=31, width=119, wrap=NONE) 
데이터보기.grid(column=0, row=1, sticky=(N,W,E,S))

# 데이터 보기 스크롤
데이터보기세로스크롤 = ttk.Scrollbar(데이터결과화면, orient=VERTICAL, command=데이터보기.yview)
데이터보기세로스크롤.grid(column=1, row=1, sticky=(N,S))
데이터보기가로스크롤 = ttk.Scrollbar(데이터결과화면, orient=HORIZONTAL, command=데이터보기.xview)
데이터보기가로스크롤.grid(column=0, row=2, sticky=(W,E))
데이터보기['yscrollcommand'] = 데이터보기세로스크롤.set
데이터보기['xscrollcommand'] = 데이터보기가로스크롤.set

# Clear 버튼
def 데이터초기화():
    global 파일이름, 속성리스트, 데이터리스트, 목적속성
    파일이름 = ''
    속성리스트 = ''
    데이터리스트 = ''
    목적속성 = ''
    파일이름입력공간.delete(0,'end')
    출력파일이름입력공간.delete(0,'end')
    데이터보기.delete('1.0',END)
    속성리스트박스.delete(0, 'end')
    속성리스트박스.insert(0, '#없음#')
    속성리스트박스1.delete(0, 'end')
    속성리스트박스1.insert(0, '#없음#')

전체초기화버튼 = ttk.Button(데이터결과화면, text='Clear', width=18, command=데이터초기화)
전체초기화버튼.grid(column=0, row=4, sticky=E)

# --------------------------------------------------------------------------------
# 종료
# --------------------------------------------------------------------------------

#창.mainloop()

# ================================================================================
# < END >
# ================================================================================

