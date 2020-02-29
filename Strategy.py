import mplfinance as mpf
import numpy as np
import Backtest
import Indicators
import yfinance as yf


# get our data
# one day timeframe
df = yf.download('BTC-USD', start='2019-01-01', end='2020-02-28')

# if you want use the ccxt dataframe :
# import Dataframe
# df = Dataframe.df

df['SMA'] = Indicators.SMA(df['Close'], 30)
# add your indicators here

# strategy in backtest
long = []
short = []
tpLong = []
tpShort = []

isLong = False
isShort = False
isTPLong = False
isTPShort = False

# hereunder an example of strategy using simple moving average in the last 30 periods (SMA30)
# you may change with your own strategy
# buy orders when current SMA30 is above last SMA30
# sell orders when current SMA30 is below last SMA30
# creation of a list for backtesting and chart purpose for every buy, sell, take profit buy, take profit sell orders
# including time and price value at candle close 
# otherwise appends NaN values

for i in range(1, len(df['Close'])):

    sma = df['SMA'][i]
    sma1 = df['SMA'][i-1]

    if not isLong and sma > sma1:
        longPrice = df['Close'][i]
        long.append([df.index[i], df['Close'][i]])
        isLong = True
        isTPLong = False
        isSLLong = False
        tpLong.append([np.nan, np.nan])
        short.append([np.nan, np.nan])
        tpShort.append([np.nan, np.nan])

    elif isLong and not isTPLong and sma < sma1:
        tpLong.append([df.index[i], df['Close'][i]])
        isLong = False
        isTPLong = True
        isSLLong = False
        long.append([np.nan, np.nan])
        short.append([np.nan, np.nan])
        tpShort.append([np.nan, np.nan])

    elif not isShort and sma < sma1:
        shortPrice = df['Open'][i]
        short.append([df.index[i], df['Close'][i]])
        isShort = True
        isTPShort = False
        isSLShort = False
        long.append([np.nan, np.nan])
        tpLong.append([np.nan, np.nan])
        tpShort.append([np.nan, np.nan])

    elif isShort and not isTPShort and sma > sma1:
        tpShort.append([df.index[i], df['Close'][i]])
        isShort = False
        isTPShort = True
        isSLShort = False
        long.append([np.nan, np.nan])
        tpLong.append([np.nan, np.nan])
        short.append([np.nan, np.nan])

    else:
        long.append([np.nan, np.nan])
        tpLong.append([np.nan, np.nan])
        short.append([np.nan, np.nan])
        tpShort.append([np.nan, np.nan])


if __name__ == '__main__':
    # call our backtest
    Backtest.backtest(df)

    # plot chart using close prices list for each order
    # append to last row NaN value
    buy = [long[i][1] for i in range(0, len(long))]
    sell = [short[i][1] for i in range(0, len(short))]
    tpbuy = [tpLong[i][1] for i in range(0, len(tpLong))]
    tpsell = [tpShort[i][1] for i in range(0, len(tpShort))]

    buy.append(np.nan)
    sell.append(np.nan)
    tpbuy.append(np.nan)
    tpsell.append(np.nan)

    # merging all components for plotting
    signals = [mpf.make_addplot(buy, scatter=True, markersize=200, marker='^', color='green'),
            mpf.make_addplot(sell, scatter=True, markersize=200, marker='v', color='red'),
            mpf.make_addplot(tpbuy, scatter=True, markersize=90, marker='s', color='green'),
            mpf.make_addplot(tpsell, scatter=True, markersize=90, marker='s', color='red')]
    # if you have other indicators, add them here in order to plot them
    # here we only have the sma, already included in command plot
    mpf.plot(df, type='candle', mav=30, addplot=signals, figscale=1.6)