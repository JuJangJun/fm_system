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
app = DjangoDash('monthly_chart')


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



############################################################################
# 월, 일별 보호구 착용여부(이분법적으로) 막대+선 그래프
############################################################################


## DB에서 값을 가져오는 함수 ##
def norm_bar_chart_data(selected_month):
    items = NormalSFView.objects.filter(month=selected_month).order_by('day')

    days = [item.day for item in items]
    normal_counts = [item.normal_cnt for item in items]
    unnormal_counts = [item.unnormal_cnt if item.unnormal_cnt is not None else 0 for item in items]

    return days, normal_counts, unnormal_counts



## 앱 레이아웃 ##
app.layout = html.Div([
    # html.H1(children='Visualize Item Quantities by Month'),
    html.Div(children='Select Month', style={'font-weight': 'bold', 'marginLeft': 20, 'marginTop': 20, 'marginBottom': 10,}),
    dcc.Dropdown(id='month-dropdown', options=get_month(), style={'marginLeft': 8, 'width':500}),
    html.Div([
        dcc.Graph(id='pie-hgv', style={'width': '50%'}),
        dcc.Graph(id='pie-chart', style={'width': '50%'})
        ], style={'display': 'flex'}),
    dcc.Graph(id='norm-bar'), 
    dcc.Interval(id='interval', interval=1*1000)  # Every 1 second
])


## 그래프를 그리고 매 초마다 업데이트하는 함수 ##
@app.callback(
    [Output('pie-hgv', 'figure'), Output('pie-chart', 'figure'), Output('norm-bar', 'figure')],
    [Input('month-dropdown', 'value'), Input('interval', 'n_intervals')]
    )

def update_graph(selected_month, n_intervals):
    labels_hgv, values_hgv = hgv_pie_chart_data(selected_month)
    fig1 = go.Figure(
        data=[go.Pie(labels=labels_hgv, values=values_hgv, textinfo='percent', textfont=dict(size=14),
                    marker=dict(colors=['rgb(255, 99, 132)',        # 분홍
                                        'rgb(255, 205, 86)',        # 노랑
                                        'rgb(104, 171, 234)',]))]   # 하늘)]
    )

    labels, values = get_pie_chart_data(selected_month)
    fig2 = go.Figure(
        data=[go.Pie(labels=labels, values=values, textinfo='percent', textfont=dict(size=14),
                    marker=dict(colors=['rgb(255, 99, 132)', 'rgb(54, 162, 235)',        # 분홍, 하늘
                                        'rgb(255, 205, 86)', 'rgb(153, 102, 255)',       # 노랑, 보라
                                        'rgb(75, 192, 192)', 'rgb(255, 159, 64)',        # 초록, 주황
                                        'rgb(130, 255, 190)', 'rgb(200, 255, 137)',]))]  # 파파초, 파초초)]
    )

    # 막대
    days, normal_counts, unnormal_counts = norm_bar_chart_data(selected_month)
    fig3 = go.Figure(data=[
        go.Bar(name='비정상 착용', x=days, y=unnormal_counts, marker_color='rgb(255, 99, 132)'),   # 분홍
        go.Bar(name='정상 착용', x=days, y=normal_counts, marker_color='rgb(54, 162, 235)'),       # 하늘
        go.Scatter(name='비정상 착용 line', x=days, y=unnormal_counts,
                            mode='lines+markers', line=dict(color='purple')),
                            ])

    fig1.update_layout(title={'text': f"<b>{selected_month}월 | 장비별 보호구 미착용 비율<b>", 'y': 0.9, 'x': 0.5,'xanchor': 'center', 'yanchor': 'top'},
                        titlefont=dict(size = 17, color='black', family='Arial, sans-serif'),
                        legend=dict(font=dict(size=14)))
    fig2.update_layout(title={'text': f"<b>{selected_month}월 | 코드별 비율<b>", 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                        titlefont=dict(size = 17, color='black', family='Arial, sans-serif'),
                        legend=dict(font=dict(size=14)))
    fig3.update_layout(barmode='stack',
                        title={'text' : f"<b>{selected_month}월 | 일별 보호구 착용 현황<b>",'y' : 0.9 ,'x' : 0.5 ,'xanchor' : "center" ,'yanchor' : "top"},
                        titlefont=dict(size = 17, color='black', family='Arial, sans-serif'),
                        legend=dict(font=dict(size=14)), plot_bgcolor="WHITE")
    
    # Update axes
    fig3.update_xaxes(title="<b>일<b>", tick0=1, dtick=1)  # Every day
    fig3.update_yaxes(title="<b>인원수<b>", tick0=0, dtick=1, gridcolor="#E6E6E6")  # Natural numbers only
    
    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)