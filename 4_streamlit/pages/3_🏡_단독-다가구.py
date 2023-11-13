import pandas as pd
import os
import geopandas as gpd
import glob
import plotly.express as px
import plotly.graph_objects as go
import folium
import json
import math
import vis_func
import streamlit as st
from datetime import datetime

from st_files_connection import FilesConnection
from PIL import Image


st.set_page_config(
    page_title="단독-다가구 대시보드",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

conn = st.experimental_connection('s3', type=FilesConnection)
@st.cache_data(ttl=3600)
def read_file_csv(filename):
  df = conn.read(filename, input_format="csv", ttl=600)
  return df 
@st.cache_data(ttl=3600)
def read_file_json(filename):
  df = conn.read(filename, input_format="json", ttl=600)
  return df





with open('4_streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    


type_option = 'sh'

sig_list = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
       '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도',
       '경상남도', '제주특별자치도']

option = st.sidebar.selectbox(
    "시군구 선택",
    sig_list
)

year_list = range(2019,2023)
year_option = st.sidebar.selectbox(
 'year',
 year_list
)

month_list = range(1,13)
month_option = st.sidebar.selectbox(
 'year',
 month_list
)

sig_area = option

trade_count_df = read_file_csv('apart-bucket/0_data/streamlit_data/trade_count.csv')
vis_trade_rent_df = read_file_csv('apart-bucket/0_data/streamlit_data/vis_trade_rent.csv')
apart_trans4 = read_file_csv('apart-bucket/0_data/streamlit_data/map_csv.csv')
sig_lat_lon = read_file_csv('apart-bucket/0_data/streamlit_data/sig_lat_lon.csv')
geo_json_seoul = read_file_json(f'apart-bucket/0_data/streamlit_data/geo_sig_{sig_area}_json.geojson')



vis_trade_rent1 = vis_func.vis_trade_rent(vis_trade_rent_df,
                          type_option,
                          sig_area,
                          year_option,
                          month_option)

trade_count1 = vis_func.trade_count(trade_count_df,
                          type_option,
                          sig_area)

trade_mean1 = vis_func.trade_mean(trade_count_df,
                          type_option,
                          sig_area)
                          
trade_mean_map1 = vis_func.trade_mean_map(apart_trans4,
                          geo_json_seoul,
                          sig_lat_lon,
                          sig_area, 
                          type_option)
                          
with st.expander("더 자세하게 알고 싶으면?",  expanded=False):
    image_col1, image_col2 = st.columns([1,4])
    with image_col1:
      image = Image.open('4_streamlit/python_book.png')
      st.image(image, width=200)  
    with image_col2:
      st.markdown("""
      ### 파이썬 데이터 분석부터 AWS 아키텍처 구축, 대시보드 제작까지!
      부동산 관련 다양한 공공 데이터를 수집하고 분석해보며 파이썬으로 데이터를 엔지니어링할 때 자주 보이는 에러와 에러 발생 이유, 그리고 문제를 해결하는 방법을 꼼꼼하게 살펴봅니다. 실제 데이터 분석 실무에서 진행하듯 공공 데이터를 가져와 전처리한 후 분석하고, 스트림릿을 활용해 시각화해봅니다. 또한, 애플리케이션으로 배포하는 것을 목표로 차근차근 AWS 아키텍처를 구축하고 보기 좋고 유의미한 대시보드를 제작합니다. 파이썬을 활용한 데이터 엔지니어링과 시각화, 그리고 대시보드 제작과 애플리케이션 배포까지 전 과정을 문제 해결의 시각으로 바라볼 수 있습니다.
        
        
      **Python을 사용한 대시보드 구성에 대한 자세한 내용을 책으로 다뤘습니다. 자세한 내용은 다음을 참고 해주세요.**
      - [데이터 분석으로 배우는 파이썬 문제 해결 (부동산 데이터 분석부터 AWS 아키텍처 구축, 대시보드 제작까지)](https://www.yes24.com/Product/Goods/123178582)
      """)      


col1, col2 = st.columns([1,1])
col1.plotly_chart(trade_mean_map1, use_container_width = True) 
col2.plotly_chart(vis_trade_rent1, use_container_width = True)


col1, col2 = st.columns([1,1])
col1.plotly_chart(trade_mean1, use_container_width = True)
col2.plotly_chart(trade_count1, use_container_width = True)




st.sidebar.markdown(
    """
    # Reference
    - [한국은행 경제통계시스템](https://ecos.bok.or.kr/#/StatisticsByTheme/VisualStat)
    - [한국은행 기준금리](https://ecos.bok.or.kr/#/SearchStat)
    - [KB 부동산 보고서](https://www.kbfg.com/kbresearch/report/reportList.do)
    - [KB 부동산 대시보드](https://data.kbland.kr/)
"""
)
