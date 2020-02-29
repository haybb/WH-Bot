import ccxt
import pandas as pd
from datetime import datetime
import Indicators


# parameters
exchange = ccxt.binance({
    'apiKey': 'paste your api key here',   
    'secret': 'paste your secret key here'})
symbol = 'BTC/USDT'
timeframe = '1d'
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
ticker = exchange.fetchTicker(symbol)

# convert timestamp to readable format + data for the graphic
dates = []
open_data = []
high_data = []
low_data = []
close_data = []

for candle in ohlcv:
    dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
    open_data.append(candle[1])
    high_data.append(candle[2])
    low_data.append(candle[3])
    close_data.append(candle[4])

# dataframe
for i in range(0, len(dates)):
    dates[i] = datetime.strptime(dates[i], '%Y-%m-%d %H:%M:%S.%f')

df = pd.DataFrame.from_records(ohlcv, dates)
df.pop(0)
df.pop(5)
col_names = ['Open', 'High', 'Low', 'Close']
df.columns = col_names
for col in col_names:
    df[col] = df[col].astype(float)

df['SMA'] = Indicators.SMA(df['Close'], 30)
# call your other indicators here

print(df)
