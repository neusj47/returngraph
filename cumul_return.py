# Ticker별 누적 수익률을 산출하는 함수

import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt

ticker = 'MSFT'
ticker_comp = 'GOOGL'

def get_price_from_yahoo(ticker):
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(ticker, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index('Date', inplace=True)
    df['returns'] = (df['Close'] / df['Close'].shift(1)) - 1
    df['cum_return'] = (1 + df['returns']).cumprod()
    return df

df = get_price_from_yahoo(ticker)
print(df)
df_comp = get_price_from_yahoo(ticker_comp)
print(df_comp)

# 그래프로 출력
df['cum_return'].plot(label=ticker,figsize=(16,8))
df_comp['cum_return'].plot(label=ticker_comp)
plt.legend()
