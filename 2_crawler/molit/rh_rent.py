# 1-1. 데이터 가져오기
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
import time
from datetime import datetime


os.chdir("/home/ubuntu/real_estate_dashboard")
print(os.getcwd())

print("시작")


directory = "0_data/molit/rh_rent"
if not os.path.exists(directory):
    os.makedirs(directory)
    

legal_info = pd.read_csv("data/legal_info.csv")
LAWD_CD_list = legal_info['법정동시군구코드'].unique()

# API키 세팅
api_key = '발급받은 API키'

column_nm = [
  '갱신요구권사용',
 '건축년도',
 '계약구분',
 '계약기간',
 '년',
 '법정동',
 '보증금액',
 '연립다세대',
 '월',
 '월세금액',
 '일',
 '전용면적',
 '종전계약보증금',
 '종전계약월세',
 '지번',
 '지역코드',
 '층'
 ]


year_month_key = '201901'

total = pd.DataFrame()
print("for 시작")
for i in range(len(LAWD_CD_list)):
    # time.sleep(2)

    # 서비스 URL
    url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHRent"

    # 요청변수 파라미터 설정     
    params = "?" + \
        "ServiceKey=" + api_key + "&" + \
        "pageNo=" + "1" + "&" + \
        "numOfRows=" + "9999" + "&" + \
        "LAWD_CD=" + str(LAWD_CD_list[i]) + "&" + \
        "DEAL_YMD=" + year_month_key

    # requests, BeautifulSoup 라이브러리를 사용한 데이터 수집
    res = requests.get(url + params)
    soup = bs(res.text, 'xml')
    items = soup.find_all('item')

    # print(str(LAWD_CD_list[i]))
    now = datetime.now()
    print(str(year_month_key) + "_" + str(LAWD_CD_list[i]) + "_" + str(i) + "_개수: " + str(len(items)) + "현재시간: "+ str(now.strftime('%Y-%m-%d %H:%M:%S')))
    
    log_data = pd.DataFrame({
        "year_month":[str(year_month_key)],
        "LAWD_CD":[str(LAWD_CD_list[i])],
        '순서':[str(i)],
        '개수': [str(len(items))],
        '시간': [str(now.strftime('%Y-%m-%d %H:%M:%S'))],
        '타입': ['연립다세대 전월세']
    })
    
    log_data.to_csv("log_data.csv", index = False, mode = 'a', header = False)

    # 수집된 데이터를 Pandas 데이터 프레임 형식으로 변환
    for k in range(len(items)):
        df_raw = []
        for j in column_nm:
            # print(LAWD_CD_list[i],k,j) # 에러 파악 여부
            try:
                items_data = items[k].find(j).text
                df_raw.append(items_data)
            except:
                items_data = None
                df_raw.append(items_data)

        df = pd.DataFrame(df_raw).T
        df.columns = column_nm
        total = pd.concat([total, df])
        
        file_name = '0_data/molit/rh_rent/rh_rent_' + str(year_month_key) + ".csv"

        if not os.path.exists(file_name):
            df.to_csv(file_name, index = False, mode = 'w')
        else:
            df.to_csv(file_name, index = False, mode = 'a', header = False)

print("=============================== 최종 완료 ==================================")
