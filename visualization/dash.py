from django.db import models

from dash import Dash, Input, Output, callback, dcc, html
from django_plotly_dash import DjangoDash

import plotly.graph_objs as go
from .models import MonthSafetyCntView


# Important: Define Id for Plotly Dash integration in Django
app = DjangoDash('dash_integration_id')



############################################################################
# DATABASE와 연결하여 DATA 불러와서 그래프 그리기
############################################################################

## DB에 저장되어있는 월(month)들을 가져오는 함수 ##
def get_month():
    month = []
    if MonthSafetyCntView.objects.exists():
        month = MonthSafetyCntView.objects.values_list('month', flat=True).distinct()
        # 빈 리스트인 경우 연도 값을 기본값으로 설정
        if not month:
            month = [2000]
    return [{'label': month, 'value': month} for month in month]

## DB에서 값을 가져오는 함수 ##
def get_pie_chart_data(selected_month):
    items = MonthSafetyCntView.objects.filter(month=selected_month)
    labels = [item.content for item in items]
    values = [item.code_count for item in items]
    
    return labels, values

## 앱 레이아웃 ##
app.layout = html.Div([
        # html.H1(children='Visualize Item Quantities by Month'),
        html.Div(children='통계 확인을 원하는 달을 고르시오'),
        dcc.Dropdown(id='month-dropdown', options=get_month(),),
        dcc.Graph(id='pie-chart'),     
        dcc.Interval(id='interval', interval=1*1000)  # Every 1 seconds
        ])

## 그래프를 그리고 매 초마다 업데이트하는 함수 ##
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('month-dropdown', 'value'), 
    Input('interval', 'n_intervals')]
    )
def update_graph(selected_month, n_intervals):
    labels, values = get_pie_chart_data(selected_month)
    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, textinfo='label+percent')]
    )
    fig.update_layout(title=f"Month {selected_month}")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)