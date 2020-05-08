from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import mplfinance as mpf
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
    df, long, short, tpLong, tpShort = Strategy.data(def_symbol.get(), def_tf.get(), def_sma_size.get())
    profit_day, profit_month = Backtest.results(df, long, short, tpLong, tpShort)
    stat_buy, projBuy = Backtest.projectionLong(df, long, tpLong)
    stat_sell, projSell = Backtest.projectionShort(df, short, tpShort)

    tit = Label(results_frame, text='Backtest results\n(with 1 unit)', font='Arial 16 underline')
    tit.grid(pady=15)

    profit = Label(results_frame, text=f'Profit/day: {profit_day}$\nProfit/month: {profit_month}%', font=('Arial', 14))
    profit.grid(pady=20)

    stb = Label(results_frame, text=f'LONG statistics:\n{stat_buy.to_string()}', font=('Arial', 14))
    stb.grid(pady=20)

    sts = Label(results_frame, text=f'SHORT statistics:\n{stat_sell.to_string()}', font=('Arial', 14))
    sts.grid(pady=20)

    if projBuy['Type'].iloc[-1] == 'buy':
       txt_last = f'Pending order:\nLONG at {round(projBuy["Values"].iloc[-1], 2)}$'
    elif projSell['Type'].iloc[-1] == 'sell':
        txt_last = f'Pending order:\nSHORT at {round(projSell["Values"].iloc[-1], 2)}$'
    pend = Label(results_frame, text=txt_last, font=('Arial', 14))
    pend.grid(pady=20)


    # plot chart with candle
    chart_frame = Frame(root)
    chart_frame.pack(fill=BOTH, expand=1)

    apds = [mpf.make_addplot(df['SMA']),
            mpf.make_addplot(df['Long'], scatter=True, marker='^', color='tab:green', markersize=80),
            mpf.make_addplot(df['TP Long'], scatter=True, marker='o', color='tab:green', markersize=80),
            mpf.make_addplot(df['Short'], scatter=True, marker='v', color='tab:red', markersize=80),
            mpf.make_addplot(df['TP Short'], scatter=True, marker='o', color='tab:red', markersize=80)]

    fig, axlist = mpf.plot(df, type='candle', returnfig=True, addplot=apds)

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

Label(settings_frame, text='SMA period', font=('Arial', 14)).grid(padx=15, column=5, row=1)
Label(settings_frame, text='Available length of Simple Moving Average: from 0 to 240',
      font=('Arial', 10)).grid(padx=15, column=1, row=4, columnspan=6)
def_sma_size = Entry(settings_frame, font=('Arial', 14), width=10)
def_sma_size.grid(padx=15, column=6, row=1)
def_sma_size.insert(0, '30')


# close user interface
def _quit():
    root.quit()
    root.destroy()


# buttons
Button(settings_frame, text='Quit', command=_quit, font=('Arial', 14)).grid(row=2, column=7)
Button(settings_frame, text='Update', font=('Arial', 14), command=updateSettings).grid(padx=10, column=7, row=1)


if __name__ == '__main__':
    root.mainloop()