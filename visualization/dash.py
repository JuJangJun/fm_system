from django.db import models

from dash import Dash, Input, Output, callback, dcc, html
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from datetime import datetime, date
from .models import MonthSafetyCntView, NormalSFView, HgvCntView


############################################################################
# 월별 보호구 미착용 비율 나타내는 파이 그래프 2개
############################################################################

# Important: Define Id for Plotly Dash integration in Django
app = DjangoDash('monthly_pie_chart')


## DB에 저장되어있는 월(month)들을 가져오는 함수 ##
def get_month():
    month = []
    if MonthSafetyCntView.objects.exists():
        month = MonthSafetyCntView.objects.values_list('month', flat=True).distinct()
        # 빈 리스트인 경우 기본값 설정
        if not month:
            month = [8]
    return [{'label': month, 'value': month} for month in month]

## 코드별 보호구 미착용 파이 그래프 ##
def get_pie_chart_data(selected_month):
    items = MonthSafetyCntView.objects.filter(month=selected_month)
    labels = [item.content for item in items]
    values = [item.code_count for item in items]
    
    return labels, values


## HGV별 보호구 미착용 파이 그래프 ##
def hgv_pie_chart_data(selected_month):
    items = HgvCntView.objects.filter(month=selected_month)

    # 첫번째 아이템 가져오기 (월은 동일하므로)
    item = items.first()

    labels_hgv = ['헬멧', '고글', '조끼']
    values_hgv = [item.helmet, item.goggle, item.vest]
    
    return labels_hgv, values_hgv


## 앱 레이아웃 ##
app.layout = html.Div([
        # html.H1(children='Visualize Item Quantities by Month'),
        html.Div(children='보고싶은 달을 선택하시오.'),
        dcc.Dropdown(id='month-dropdown', options=get_month(),),
        html.Div([dcc.Graph(id='pie-chart'),
                dcc.Graph(id='pie-hgv'),], style={'display': 'flex'}),
        dcc.Interval(id='interval', interval=1*1000)  # Every 1 seconds
        ])

## 그래프를 그리고 매 초마다 업데이트하는 함수 ##
@app.callback(
    [Output('pie-chart', 'figure'), Output('pie-hgv', 'figure')],
    [Input('month-dropdown', 'value'), Input('interval', 'n_intervals')]
    )
def update_graph(selected_month, n_intervals):
    labels, values = get_pie_chart_data(selected_month)
    fig1 = go.Figure(
        data=[go.Pie(labels=labels, values=values, textinfo='label+percent')]
    )

    labels_hgv, values_hgv = hgv_pie_chart_data(selected_month)
    fig2 = go.Figure(
        data=[go.Pie(labels=labels_hgv, values=values_hgv, textinfo='label+percent')]
    )

    fig1.update_layout(title=f"{selected_month}월달 코드별 보호구 미착용 비율")
    fig2.update_layout(title=f"{selected_month}월달 장비별 보호구 미착용 비율")
    
    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)


############################################################################
# 월, 일별 보호구 착용여부(이분법적으로) 막대+선 그래프
############################################################################

app = DjangoDash('norm_bar_graph')

## DB에 저장되어있는 월(month)들을 가져오는 함수 ##
def get_month_norm():
    month = []
    if NormalSFView.objects.exists():
        month = NormalSFView.objects.values_list('month', flat=True).distinct()
        # 빈 리스트인 경우 연도 값을 기본값으로 설정
        if not month:
            month = [8]
    return [{'label': month, 'value': month} for month in month]

## DB에서 값을 가져오는 함수 ##
def norm_bar_chart_data(selected_month):
    items = NormalSFView.objects.filter(month=selected_month).order_by('day')

    days = [item.day for item in items]
    normal_counts = [item.normal_cnt for item in items]
    unnormal_counts = [item.unnormal_cnt for item in items]

    return days, normal_counts, unnormal_counts

## 앱 레이아웃 ##
app.layout = html.Div([
        # html.H1(children='Visualize Item Quantities by Month'),
        html.Div(children='보고싶은 달을 선택하시오.'),
        dcc.Dropdown(id='norm-dropdown', options=get_month_norm(),),
        dcc.Graph(id='norm-bar'),     
        dcc.Interval(id='norm-interval', interval=1*1000)  # Every 1 seconds
        ])

## 그래프를 그리고 매 초마다 업데이트하는 함수 ##
@app.callback(
    Output('norm-bar', 'figure'),
    [Input('norm-dropdown', 'value'), Input('norm-interval', 'n_intervals')]
    )
def update_graph(selected_month, n_intervals):
    days, normal_counts, unnormal_counts = norm_bar_chart_data(selected_month)
    
    # 선 그래프의 마커가 막대 그래프의 중간을 지나도록 하기 위한 변수 설정
    centered_days = [day + 0.2 for day in days]

    fig = go.Figure(data=[
        go.Bar(name='Normal', x=days, y=normal_counts),
        go.Bar(name='Unnormal', x=days, y=unnormal_counts),
        go.Scatter(name='Unnormal Line', x=centered_days, y=unnormal_counts,
                            mode='lines+markers', line=dict(color='purple'))
        ])
    
    fig.update_layout(barmode='group',
                    title=f"{selected_month}월달 일별 보호구 착용 여부",
                    xaxis_title="일",
                    yaxis_title="사람 수(명)")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)