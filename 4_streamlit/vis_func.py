import pandas as pd
import os
import geopandas as gpd
import glob
import plotly.express as px
import plotly.graph_objects as go
import folium
import json
import math
from plotly.validators.scatter.marker import SymbolValidator



def readNumber(n):
    if(n > 10**4):
        a = str(format(math.floor(n / 10**4),',d')) + '억'
        b = ' ' + str(format(math.floor(n % 10**4),',d'))
        c = a + b
    else:
        c = format(n,',d')
    return(c)

def map_trade(df, trade_option,
              amount_value_0,amount_value_1, 
              area_value_0, area_value_1, 
              year_value_0, year_value_1,
              floor_value_0, floor_value_1):
    
    if(trade_option == '매매'):
        df_trade_202210_2 = df                
        apt_trade_202210_3 = df_trade_202210_2[
          (df_trade_202210_2['거래금액'] >= amount_value_0) & 
          (df_trade_202210_2['거래금액'] <= amount_value_1) &
          (df_trade_202210_2['전용면적'] >= area_value_0) & 
          (df_trade_202210_2['전용면적'] <= area_value_1) &
          (df_trade_202210_2['사용승인일'] >= year_value_0) & 
          (df_trade_202210_2['사용승인일'] <= year_value_1) & 
          (df_trade_202210_2['층'] >= floor_value_0) & 
          (df_trade_202210_2['층'] <= floor_value_1)
          ]
        
        if('아파트' in df.columns):
            apt_trade_202210_3['이름'] = apt_trade_202210_3['아파트']
        elif('연립다세대' in df.columns):
            apt_trade_202210_3['법정동'] = apt_trade_202210_3['동리명']
            apt_trade_202210_3['이름'] = apt_trade_202210_3['연립다세대']
        elif('단지' in df.columns):
            apt_trade_202210_3['이름'] = apt_trade_202210_3['단지']
            apt_trade_202210_3['법정동'] = apt_trade_202210_3['동리명']
        
        apt_trade_202210_3['거래금액_int'] = apt_trade_202210_3['거래금액'].astype(int)
        apt_trade_202210_3['거래금액'] = apt_trade_202210_3['거래금액_int'].apply(readNumber)
    
        fig = px.scatter_mapbox(apt_trade_202210_3,
                                lat="lat",
                                lon="lon",
                                hover_data={
                                  "lat" : False,
                                  "lon" : False,
                                  "이름" : True,
                                  "법정동": True,
                                  "거래금액": True,
                                  "거래금액_int": False,
                                  "전용면적":True,
                                  },
                                color = '시군구명',
                                size = '거래금액_int',
                                height = 600,
                                zoom=10)
        
    
    # 전세
    elif(trade_option == '전세') :
        df_trade_202210_2 = df[df['월세금액'] == 0]             
        apt_trade_202210_3 = df_trade_202210_2[
          (df_trade_202210_2['보증금액'] >= amount_value_0) & 
          (df_trade_202210_2['보증금액'] <= amount_value_1) &
          (df_trade_202210_2['전용면적'] >= area_value_0) & 
          (df_trade_202210_2['전용면적'] <= area_value_1) &
          (df_trade_202210_2['사용승인일'] >= year_value_0) & 
          (df_trade_202210_2['사용승인일'] <= year_value_1) & 
          (df_trade_202210_2['층'] >= floor_value_0) & 
          (df_trade_202210_2['층'] <= floor_value_1)
          ]
        
        if('아파트' in df.columns):
            apt_trade_202210_3['이름'] = apt_trade_202210_3['아파트']
            apt_trade_202210_3['법정동'] = apt_trade_202210_3['동리명']
        elif('연립다세대' in df.columns):
            apt_trade_202210_3['법정동'] = apt_trade_202210_3['동리명']
            apt_trade_202210_3['이름'] = apt_trade_202210_3['연립다세대']
        elif('단지' in df.columns):
            apt_trade_202210_3['이름'] = apt_trade_202210_3['단지']
            apt_trade_202210_3['법정동'] = apt_trade_202210_3['동리명']
        
        apt_trade_202210_3['보증금액_int'] = apt_trade_202210_3['보증금액'].astype(int)
        apt_trade_202210_3['보증금액'] = apt_trade_202210_3['보증금액_int'].apply(readNumber)
        
        fig = px.scatter_mapbox(apt_trade_202210_3,
                                lat="lat",
                                lon="lon",
                                hover_data={
                                  "lat" : False,
                                  "lon" : False,
                                  "이름" : True,
                                  "법정동": True,
                                  "보증금액": True,
                                  "보증금액_int": False,
                                  "전용면적":True,
                                  },
                                color = '시군구명',
                                size = '보증금액_int',
                                height = 600,
                                zoom=10)
        
    elif(trade_option == '월세') :
        df_trade_202210_2 = df[df['월세금액'] != 0]             
        apt_trade_202210_3 = df_trade_202210_2[
          (df_trade_202210_2['보증금액'] >= amount_value_0) & 
          (df_trade_202210_2['보증금액'] <= amount_value_1) &            
          (df_trade_202210_2['전용면적'] >= area_value_0) & 
          (df_trade_202210_2['전용면적'] <= area_value_1) &
          (df_trade_202210_2['사용승인일'] >= year_value_0) & 
          (df_trade_202210_2['사용승인일'] <= year_value_1) & 
          (df_trade_202210_2['층'] >= floor_value_0) & 
          (df_trade_202210_2['층'] <= floor_value_1)
          ]
        
        if('아파트' in df.columns):
            apt_trade_202210_3['이름'] = apt_trade_202210_3['아파트']
            apt_trade_202210_3['법정동'] = apt_trade_202210_3['동리명']
        elif('연립다세대' in df.columns):
            apt_trade_202210_3['법정동'] = apt_trade_202210_3['동리명']
            apt_trade_202210_3['이름'] = apt_trade_202210_3['연립다세대']
        elif('단지' in df.columns):
            apt_trade_202210_3['이름'] = apt_trade_202210_3['단지']
            apt_trade_202210_3['법정동'] = apt_trade_202210_3['동리명']
        
        apt_trade_202210_3['보증금액_int'] = apt_trade_202210_3['보증금액'].astype(int)
        apt_trade_202210_3['보증금액'] = apt_trade_202210_3['보증금액_int'].apply(readNumber)
        
        fig = px.scatter_mapbox(apt_trade_202210_3,
                                lat="lat",
                                lon="lon",
                                hover_data={
                                  "lat" : False,
                                  "lon" : False,
                                  "이름" : True,
                                  "법정동": True,
                                  "보증금액": True,
                                  "보증금액_int": False,
                                  "전용면적":True,
                                  },
                                color = '시군구명',
                                size = '보증금액_int',
                                height = 600,
                                zoom=10)
        
    fig.update_layout(
      mapbox_style="carto-positron",
      coloraxis_showscale=False,
      showlegend=False,
      margin={"r":0,"t":0,"l":0,"b":0},
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
        ),
        template='plotly_white'
      )
      
    
          
    return(fig)


def trade_mean_map(trade_mean_df,geo_json_seoul,sig_lat_lon,sig_area,type_val):
  
    type_dic = {'apt':'아파트', 'rh':'연립다세대','sh':'단독-다가구','offi':'오피스텔'}
    type_nm = type_dic[type_val]
  
    trade_mean_df_1 = trade_mean_df[trade_mean_df['시도명'] == sig_area]
    sig_lat_lon_info = sig_lat_lon[sig_lat_lon['sig_nm'] == sig_area].reset_index(drop = True)
    
    trade_mean_df_1['거래금액_int'] = trade_mean_df_1['거래금액'].astype(int)
    trade_mean_df_1['거래금액'] = trade_mean_df_1['거래금액_int'].apply(readNumber)
        
    fig = px.choropleth_mapbox(trade_mean_df_1, 
                               geojson=geo_json_seoul, 
                               color="거래금액_int",
                               color_continuous_scale="Reds",
                               hover_data={
                                   "SIG_CD" : False,
                                   "시도명" : True,
                                   "시군구명" : True,
                                   "거래금액": True,
                                   "거래금액_int": False
                               },
                               locations="SIG_CD", 
                               featureidkey="properties.SIG_CD",
                               center={"lat":sig_lat_lon_info['lon'][0], 
                                       "lon":sig_lat_lon_info['lat'][0]},
                               mapbox_style="carto-positron",
                               zoom=9)
    
    fig.update_layout(
      margin={"r":0,"t":50,"l":0,"b":0},
      title = f'{sig_area} 시군구별 {type_nm} 매매 거래금액 지도',
      title_font_family="맑은고딕",
      title_font_size = 18,
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
        ),
        template='plotly_white'
    
      )
      
    return fig  


def vis_trade_rent(total, type_val, sig_area, year_val, month_val):

    type_dic = {'apt':'아파트', 'rh':'연립다세대','sh':'단독-다가구','offi':'오피스텔'}
    type_nm = type_dic[type_val]
    
    total['년'] = total['년'].astype(int)
    total['월'] = total['월'].astype(int)
    total['mean'] = total['mean'].astype(int)
    total['mean_2'] = total['mean'].apply(readNumber)

    df1 = total[(total['시도명'] == sig_area) & 
                (total['년'] == year_val) & 
                (total['월'] == month_val) & 
                (total['타입'] == type_val)]


    df1 = df1.sort_values(by = 'mean',ascending=False)


    fig = go.Figure(data = [
        go.Bar(name = '매매',
               y = df1[df1['구분'] == '매매']['mean'], 
               x = df1[df1['구분'] == '매매']['시군구명'], 
               # marker_color='crimson',
               marker_color='black',
               opacity=1,
               marker_pattern_shape="-",
               text = df1[df1['구분'] == '매매']['mean_2'],
               hovertemplate='%{text}만'
              ),
        go.Bar(name = '전세', 
               y = df1[df1['구분'] == '전세']['mean'], 
               x = df1[df1['구분'] == '전세']['시군구명'],
#                marker_color='blue',
               marker_color='black',
               opacity=0.7,
               marker_pattern_shape="x",
               text = df1[df1['구분'] == '전세']['mean_2'],
               hovertemplate='%{text}만'
              ),
        go.Bar(name = '월세',
               y = df1[df1['구분'] == '월세']['mean'], 
               x = df1[df1['구분'] == '월세']['시군구명'],
#                marker_color='green',
               marker_color='black',
               opacity=0.3,
               marker_pattern_shape="+",
               text = df1[df1['구분'] == '월세']['mean_2'],
               hovertemplate='%{text}만'
              ),
    ])



    fig.update_layout(
        title= f'{sig_area} 시군구별 {type_nm} 매매(실거래가)/전월세(보증금) 평균 <br><sup>단위(만원)</sup>',
        title_font_family="맑은고딕",
        title_font_size = 18,
        hoverlabel=dict(
            bgcolor='white',
            font_size=15,
        ),
        hovermode="x unified",
        template='plotly_white', 
        xaxis_tickangle=90,
        yaxis_tickformat = ',',
        legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), #Adjust legend position
        barmode='group'
    )

    return(fig)
  

def trade_count(df_trade, type_val, sig_area):
    
    type_dic = {'apt':'아파트', 'rh':'연립다세대','sh':'단독-다가구','offi':'오피스텔'}
    type_nm = type_dic[type_val]

    total = df_trade
    df1 = total[(total['시도명'] == sig_area) & 
                (total['타입'] == type_val)]
    fig = go.Figure(data=[
        go.Scatter(
            name = '매매', 
            x=df1[df1['구분'] == '매매']['거래날짜'],
            y=df1[df1['구분'] == '매매']['count'],
            hovertemplate='%{y}건',
            marker_size=8,                   
            line_shape='spline'),

        go.Scatter(
            name = '전세', 
            x=df1[df1['구분'] == '전세']['거래날짜'],
            y=df1[df1['구분'] == '전세']['count'],
            hovertemplate='%{y}건',
            marker_symbol='triangle-down',
            marker_size=8,                 
            line_shape='spline'),

          go.Scatter(
            name = '월세',
            x=df1[df1['구분'] == '월세']['거래날짜'],
            y=df1[df1['구분'] == '월세']['count'],
            hovertemplate='%{y}건',
            marker_symbol='square',
            marker_size=8,
            line_shape='spline')
        ])

    fig.update_traces(mode='lines+markers')

    fig.update_layout(
        title= f'{sig_area} 시군구별 {type_nm} 매매(실거래가)/전월세(보증금) 거래량',
      title_font_family="맑은고딕",
      title_font_size = 18,
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
      ),
      hovermode="x unified",
      template='plotly_white', 
      xaxis_tickangle=90,
      yaxis_tickformat = ',',
      legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), 
      barmode='group'
    )

    for i in range(2019, 2023):
        fig.add_vline(x=f'{i}-01-01', line_width=1, line_dash="dash", line_color="green")
    return(fig)
  
  
def trade_mean(df_trade, type_val, sig_area):

    type_dic = {'apt':'아파트', 'rh':'연립다세대','sh':'단독-다가구','offi':'오피스텔'}
    type_nm = type_dic[type_val]
    
    total = df_trade
    df1 = total[(total['시도명'] == sig_area) &
                (total['타입'] == type_val)]
                
    df1['mean'] = df1['mean'].astype(int)
    df1['mean_2'] = df1['mean'].apply(readNumber)
    
    fig = go.Figure(data=[
        go.Scatter(
            name = '매매',
            x=df1[df1['구분'] == '매매']['거래날짜'],
            y=df1[df1['구분'] == '매매']['mean'],
            text = df1[df1['구분'] == '매매']['mean_2'],
            hovertemplate='%{text}만',
            marker_size=8,                
            line_shape='spline'),

        go.Scatter(
            name = '전세',
            x=df1[df1['구분'] == '전세']['거래날짜'],
            y=df1[df1['구분'] == '전세']['mean'],
            text = df1[df1['구분'] == '전세']['mean_2'],
            hovertemplate='%{text}만',
            marker_symbol='triangle-down',
            marker_size=8,                
            line_shape='spline'),

          go.Scatter(
            name = '월세',
            x=df1[df1['구분'] == '월세']['거래날짜'],
            y=df1[df1['구분'] == '월세']['mean'],
            text = df1[df1['구분'] == '월세']['mean_2'],
            hovertemplate='%{text}만',
            marker_symbol='square',
            marker_size=8,              
            line_shape='spline')
        ])

    # fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_traces(mode='lines+markers')

    fig.update_layout(
        title= f'{sig_area} 시군구별 {type_nm} 매매(실거래가)/전월세(보증금) 평균 <br><sup>단위(만원)</sup>',
      title_font_family="맑은고딕",
      title_font_size = 18,
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
      ),
      hovermode="x unified",
      template='plotly_white',
      xaxis_tickangle=90,
      yaxis_tickformat = ',',
      legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), 
      barmode='group'
    )

    for i in range(2019, 2023):
        fig.add_vline(x=f'{i}-01-01', line_width=1, line_dash="dash", line_color="green")
    return(fig)

  

def cencus_count(df_raw, sig_area):
  
    df_raw = df_raw[df_raw['행정동_시도명'] == sig_area]
    df_raw = df_raw.reset_index(drop = True)

    df_vis = df_raw[['행정동_시군구명', '인구수', '구분']].groupby(['행정동_시군구명','구분']).sum()
    df_vis = df_vis.reset_index()
    df_vis = df_vis.sort_values(by = '인구수',ascending=False)

    fig = go.Figure(data=[
    go.Bar(
      name = '총인구수', 
      x=df_vis[df_vis['구분'] == '총인구수']['행정동_시군구명'],
      y=df_vis[df_vis['구분'] == '총인구수']['인구수'],
      hovertemplate='%{y}명'
    ),

    go.Bar(
      name = '남자인구수', 
      x=df_vis[df_vis['구분'] == '남자인구수']['행정동_시군구명'],
      y=df_vis[df_vis['구분'] == '남자인구수']['인구수'],
      hovertemplate='%{y}명'
    ),

    go.Bar(
      name = '여자인구수',
      x=df_vis[df_vis['구분'] == '여자인구수']['행정동_시군구명'],
      y=df_vis[df_vis['구분'] == '여자인구수']['인구수'],
      hovertemplate='%{y}명'

    )
    ])


    fig.update_layout(
        title= f'{sig_area} 시군구별 지역별 인구수 <br><sup>단위(명)</sup>',
        title_font_family="맑은고딕",
        title_font_size = 18,
        hoverlabel=dict(
            bgcolor='white',
            font_size=15,
        ),
        hovermode="x unified",
        template='plotly_white', 
        xaxis_tickangle=90,
        yaxis_tickformat = ',',
        legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), #Adjust legend position
        barmode='group'
    )

    return(fig)
  
  
def school_count(df_school, sig_area):
  
    df_school_1 = df_school[df_school['시도명'] == sig_area]
    df_school_1 = df_school_1.reset_index(drop = True)


    df_school_1 = df_school_1[['시군구명','설립명','학교명']].groupby(['시군구명','설립명']).describe()
    df_school_1 = df_school_1.reset_index()

    apart_trans2 = pd.concat([df_school_1[['시군구명','설립명']],df_school_1['학교명'][['count']]], axis = 1)
    apart_trans2.columns = ['시군구명','설립명','count']
    apart_trans2 = apart_trans2.sort_values(by = 'count',ascending=False)

    
    fig = go.Figure(data=[
        go.Bar(
          name = '사립', 
          x=apart_trans2[apart_trans2['설립명'] == '사립']['시군구명'],
          y=apart_trans2[apart_trans2['설립명'] == '사립']['count'],
          hovertemplate='%{y}개'
        ),

        go.Bar(
          name = '공립', 
          x=apart_trans2[apart_trans2['설립명'] == '공립']['시군구명'],
          y=apart_trans2[apart_trans2['설립명'] == '공립']['count'],
          hovertemplate='%{y}개'
        ),

        go.Bar(
          name = '국립',
          x=apart_trans2[apart_trans2['설립명'] == '국립']['시군구명'],
          y=apart_trans2[apart_trans2['설립명'] == '국립']['count'],
          hovertemplate='%{y}개'

        )
        ])


    fig.update_layout(
            title= f'{sig_area} 시군구별 초등학교 수 <br><sup>단위(명)</sup>',
            title_font_family="맑은고딕",
            title_font_size = 18,
            hoverlabel=dict(
                bgcolor='white',
                font_size=15,
            ),
            hovermode="x unified",
            template='plotly_white', 
            xaxis_tickangle=90,
            yaxis_tickformat = ',',
            legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), #Adjust legend position
            barmode='group'
        )

    return(fig)

  
def park_count(park_raw, sig_area):
  
    park_raw = park_raw[park_raw['시도명'] == sig_area]
    park_raw = park_raw.reset_index(drop = True)
    
    park_raw = park_raw[['시군구명','공원구분','공원명']].groupby(['시군구명','공원구분']).describe()
    park_raw = park_raw.reset_index()

    park_vis = pd.concat([park_raw[['시군구명','공원구분']],park_raw['공원명'][['count']]], axis = 1)
    park_vis.columns = ['시군구명','공원구분','count']
    
    fig = go.Figure()
    key_list = park_vis['공원구분'].unique()
    for key in key_list:
        fig.add_trace(go.Bar(
          name = key,
          x=park_vis[park_vis['공원구분'] == key]['시군구명'],
          y=park_vis[park_vis['공원구분'] == key]['count'],
          hovertemplate='%{y}개'
        )
        )


    fig.update_layout(
        title= f'{sig_area} 시군구별 도시 공원 개수 <br><sup>단위(개)</sup>',
        title_font_family="맑은고딕",
        title_font_size = 18,
        hoverlabel=dict(
            bgcolor='white',
            font_size=15,
        ),
        hovermode="x unified",
        template='plotly_white', 
        xaxis_tickangle=90,
        yaxis_tickformat = ',',
        legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), #Adjust legend position
        barmode='stack'
    )

    return(fig)
  
def park_geo(park_raw, sig_area):
    public_park_df = park_raw[park_raw['시도명'] == sig_area]
    fig = px.scatter_mapbox(public_park_df,
                            lat="위도",
                            lon="경도",
                            color="공원구분",
                            hover_data={
                              "위도" : False,
                              "경도" : False,
                              "공원명" : True,
                              "공원구분": True,
                              "소재지지번주소": True
                              },
                            zoom = 10,
                            title = f'{sig_area} 시군구별 도시 공원 위치'
                              )

      
    fig.update_layout(
      mapbox_style="carto-positron",
      margin={"r":0,"t":50,"l":0,"b":0},
      hoverlabel=dict(
        bgcolor='white',
        font_size=15,
        ),
        template='plotly_white'
      )
        
    return(fig)
