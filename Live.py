import ccxt
from datetime import datetime
import pandas as pd
import time
import schedule
import numpy as np


long = []
short = []
tpLong = []
tpShort = []

isLong = False
isShort = False
isTPLong = False
isTPShort = False

pricebuy = []
pricesell = []

profitSell = []
profitBuy = []
lastProfit = 0


def main():
    exchange = ccxt.binance({
        'apiKey': 'paste your api key here',
        'secret': 'paste your secret key here'})

    symbol = 'BTC/USDT'
    timeframe = '4h'
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    amount = 0.1 # BTC

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

    df = pd.DataFrame.from_records(ohlcv, dates)
    df.pop(0)
    df.pop(5)
    col_names = ['Open', 'High', 'Low', 'Close']
    df.columns = col_names
    for col in col_names:
        df[col] = df[col].astype(float)

    def SMA(data, period):
        return [np.mean(data[idx - (period - 1):idx + 1]) for idx in range(0, len(data))]

    df['SMA'] = SMA(df['Close'], 30)

    # backtest
    ticker = exchange.fetchTicker(symbol)
    timedate = ticker['datetime']
    last = ticker['last']
    sma = df['SMA'][-1]
    sma1 = df['SMA'][-2]

    global lastProfit, long, short, tpLong, tpShort, profitSell, profitBuy, isLong, isShort, isTPLong, isTPShort


    # live
    if not isLong and sma > sma1:
        pricebuy.append(last)
        long.append([timedate, last])
        isLong = True
        isTPLong = False
        marketBuy = exchange.create_market_buy_order(symbol, amount, {'test': True})
        print(timedate, 'LONG at', pricebuy[-1])

    elif isLong and not isTPLong and sma < sma1:
        tpLong.append([timedate, last])
        isLong = False
        isTPLong = True
        marketSell = exchange.create_market_sell_order(symbol, amount, {'test': True})
        profitBuy.append(last - long[-1][1])
        print(timedate, 'TP LONG at', last, 'profit made:', profitBuy[-1],'\n')
        time.sleep(5)

    elif not isShort and sma < sma1:
        short.append([timedate, last])
        pricesell.append(last)
        isShort = True
        isTPShort = False
        marketSell = exchange.create_market_sell_order(symbol, amount, {'test': True})
        print(timedate, 'SHORT at', pricesell[-1])

    elif isShort and not isTPShort and sma > sma1:
        tpShort.append([timedate, last])
        isShort = False
        isTPShort = True
        marketBuy = exchange.create_market_buy_order(symbol, amount, {'test': True})
        profitSell.append(-last + short[-1][1])
        print(timedate, 'TP SHORT at', last, 'profit made:', profitSell[-1], '\n')
        time.sleep(5)


    totalProfit = round(sum(profitBuy) + sum(profitSell), 2)
    if lastProfit != totalProfit:
        lastProfit = totalProfit
        print('Total profit:', totalProfit, '\n')


if __name__ == '__main__':

    print('\nStart at', datetime.now(), '\n')
    schedule.every(4).hours.at(":01").do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(1)















