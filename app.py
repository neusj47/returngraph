# -*- coding: utf-8 -*-

# Ticker별 누적 수익률을 산출하는 함수
# 날짜, 관심 TICKER를 입력하여 누적 수익률 추이를 확인합니다.
# 반응형 그래프를 만들기 위해 Callback 함수를 정의합니다.
# 누적 수익률은 종가/전일종가 -1 로 산출한 수익률을 pandas의 cumprod() 함수를 이용하여 산출합니다.

import pandas_datareader.data as web
import datetime
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# 시작일자를 입력합니다.
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime.now()

# dashboard add을 실행합니다.
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Cumulative return chart'),
    html.Div(children='''
    Enter the TICKER you want to compare
    ** vice versa is ok 
    '''),
    dcc.Input(id='input', value='', type='text', placeholder="ex) TSLA"),
    html.Div(id='output-graph'),
    dcc.Input(id='input-comp', value='', type='text', placeholder="ex) AMZN"),
    html.Div(id='output-graph-comp')
])

# Callback함수를 정의합니다. (Input = 'input', Output = 'output_graph')
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
# 반응형 그래프를 위해 Update_value 함수를 정의합니다.
def update_value(input_data):
    df = web.DataReader(input_data, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    df['returns'] = (df['Close'] / df['Close'].shift(1)) - 1
    df['cum_return'] = (1 + df['returns']).cumprod()

    return dcc.Graph(
        id='price-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df.cum_return, 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )

# 비교 대상을 위한 Callback 함수를 정의 합니다.
@app.callback(
    Output(component_id='output-graph-comp', component_property='children'),
    [Input(component_id='input-comp', component_property='value')]
)
# 반응형 그래프를 위해 Update_value 함수를 정의합니다.
def update_value(input_data):
    df = web.DataReader(input_data, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    df['returns'] = (df['Close']/df['Close'].shift(1))-1
    df['cum_return'] = (1 + df['returns']).cumprod()

    return dcc.Graph(
        id='price-graph-comp',
        figure={
            'data': [
                {'x': df.index, 'y': df.cum_return, 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)