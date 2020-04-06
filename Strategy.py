import numpy as np
import Indicators
import yfinance as yf


def data(symbol, timeframe, sma_len):

    # get our data
    # valid downloadable periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    df = yf.download(symbol, period='1y', interval=timeframe)

    df['SMA'] = Indicators.SMA(df['Close'], int(sma_len))
    # should you wish to use another strategy
    # add your indicators here

    buy = []
    sell = []
    tpbuy = []
    tpsell = []

    for i in range(0, len(df['Close'])):
        buy.append(np.nan)
        tpbuy.append(np.nan)
        sell.append(np.nan)
        tpsell.append(np.nan)

    df['Long'] = buy
    df['Short'] = sell
    df['TP Long'] = tpbuy
    df['TP Short'] = tpsell


    # strategy in backtest
    long = []
    short = []
    tpLong = []
    tpShort = []

    isLong = False
    isShort = False
    isTPLong = False
    isTPShort = False

    '''hereunder an example of strategy using simple moving average in the last X periods (SMA)
    you may change with your own strategy
    buy orders when current SMA is above last SMA
    sell orders when current SMA is below last SMA
    creation of a list for backtesting and chart purpose for every buy, sell, take profit buy, take profit sell orders
    including time and price value at candle close'''

    for i in range(1, len(df['Close'])):

        sma = df['SMA'][i]
        sma1 = df['SMA'][i-1]

        if not isLong and sma > sma1:
            long.append([df.index[i], df['Close'][i]])
            df['Long'][i] = df['Close'][i]
            isLong = True
            isTPLong = False

        elif isLong and not isTPLong and sma < sma1:
            tpLong.append([df.index[i], df['Close'][i]])
            df['TP Long'][i] = df['Close'][i]
            isLong = False
            isTPLong = True

        elif not isShort and sma < sma1:
            short.append([df.index[i], df['Close'][i]])
            df['Short'][i] = df['Close'][i]
            isShort = True
            isTPShort = False

        elif isShort and not isTPShort and sma > sma1:
            tpShort.append([df.index[i], df['Close'][i]])
            df['TP Short'][i] = df['Close'][i]
            isShort = False
            isTPShort = True

    return df, long, short, tpLong, tpShort