from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.dates import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mplfinance.original_flavor import candlestick_ohlc
import Strategy
import Backtest


# main screen initial settings
root = Tk()
root.title('WH Bot')
root.state('zoomed')
root.minsize(1100, 600)
root.iconbitmap('Images\investment.ico')


# split main screen in frames
chart_frame = Frame(root)

results_frame = Frame(root)
results_frame.pack(side='left')

settings_frame = Frame(root)
settings_frame.pack(side='top')


# avoid labels ovlerlaps
tit = Label(results_frame)
profit = Label(results_frame)
stb = Label(results_frame)
sts = Label(results_frame)
pend = Label(results_frame)
fig, ax = plt.subplots(1)
canvas = FigureCanvasTkAgg(fig, chart_frame)
toolbar = NavigationToolbar2Tk(canvas, chart_frame)


# update settings & results frames and graph with Tkinter
def updateSettings():

    global profit, stb, sts, pend, fig, ax, canvas, toolbar, chart_frame, tit
    tit.destroy()
    profit.destroy()
    stb.destroy()
    sts.destroy()
    pend.destroy()
    chart_frame.destroy()

    # frame results
    Strategy.data(def_symbol.get(), def_tf.get(), def_sma_size.get())
    profit_day, profit_month = Backtest.results(Strategy.df)

    tit = Label(results_frame, text='Backtest results\n(with 1 unit)', font='Arial 16 underline')
    tit.grid(pady=15)

    profit = Label(results_frame, text='Profit/day: ' + str(profit_day) + '$\nProfit/month: '
                                       + str(profit_month) + '%', font=('Arial', 14))
    profit.grid(pady=20)

    stb = Label(results_frame, text='LONG statistics:\n' + str(Backtest.stat_buy.to_string()), font=('Arial', 14))
    stb.grid(pady=20)

    sts = Label(results_frame, text='SHORT statistics:\n' + str(Backtest.stat_sell.to_string()), font=('Arial', 14))
    sts.grid(pady=20)

    projBuy = Backtest.projBuy
    projSell = Backtest.projSell
    if projBuy['Type'].iloc[-1] == 'buy':
       txt_last = 'Pending order:\nLONG at ' + str(round(projBuy['Values'].iloc[-1], 2)) + '$'
    elif projSell['Type'].iloc[-1] == 'sell':
        txt_last = 'Pending order:\nSHORT at ' + str(round(projSell['Values'].iloc[-1], 2)) + '$'
    pend = Label(results_frame, text=txt_last, font=('Arial', 14))
    pend.grid(pady=20)


    # plot chart with candle
    chart_frame = Frame(root)
    chart_frame.pack(fill=BOTH, expand=1)

    # first reset the date
    df = Strategy.df
    df_reset = df.loc[:].reset_index()
    df_reset['date_ax'] = df_reset['Date'].apply(lambda date: date2num(date))
    df_values = [tuple(vals) for vals in df_reset[['date_ax', 'Open', 'High', 'Low', 'Close']].values]

    # set time on axis
    months = MonthLocator()
    days = DayLocator()
    weekFormatter = DateFormatter('%b %d')

    # then plot
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_major_formatter(weekFormatter)

    ax.plot(df['Long'], marker='^', color='b', markersize=7, label='Buy')
    ax.plot(df['TP Long'], marker='o', color='b', markersize=7, label='Close Buy')
    ax.plot(df['Short'], marker='v', color='y', markersize=7, label='Sell')
    ax.plot(df['TP Short'], marker='o', color='y', markersize=7, label='Close Sell')
    ax.plot(df['SMA'], color='k')

    candlestick_ohlc(ax, df_values, width=0.6, colorup='g', colordown='r')
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price ($)')

    plt.title(str(def_symbol.get()) + ' ' + str(def_tf.get()))
    ax.legend()

    # embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, chart_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)


# settings frame
Label(settings_frame, text='Market', font=('Arial', 14)).grid(padx=15, column=1, row=1)
Label(settings_frame, text='Available markets: all available on Yahoo Finance',
      font=('Arial', 10)).grid(padx=15, column=1, row=2, columnspan=6)
def_symbol = Entry(settings_frame, font=('Arial', 14), width=10)
def_symbol.grid(padx=15, column=2, row=1)
def_symbol.insert(0, 'BTC-USD')

Label(settings_frame, text='Timeframe', font=('Arial', 14)).grid(padx=15, column=3, row=1)
Label(settings_frame, text='Available timeframes: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo',
      font=('Arial', 10)).grid(padx=15, column=1, row=3, columnspan=6)
def_tf = Entry(settings_frame, font=('Arial', 14), width=10)
def_tf.grid(padx=15, column=4, row=1)
def_tf.insert(0, '1d')

Label(settings_frame, text='SMA length', font=('Arial', 14)).grid(padx=15, column=5, row=1)
Label(settings_frame, text='Available length of Simple Moving Average: from 0 to 240',
      font=('Arial', 10)).grid(padx=15, column=1, row=4, columnspan=6)
def_sma_size = Entry(settings_frame, font=('Arial', 14), width=10)
def_sma_size.grid(padx=15, column=6, row=1)
def_sma_size.insert(0, '50')


# close user interface
def _quit():
    root.quit()
    root.destroy()


# buttons
Button(settings_frame, text='Quit', command=_quit, font=('Arial', 14)).grid(row=2, column=7)
Button(settings_frame, text='Update', font=('Arial', 14), command=updateSettings).grid(padx=10, column=7, row=1)


if __name__ == '__main__':
    root.mainloop()
