import pandas as pd
from datetime import datetime


projBuy = pd.DataFrame()
projSell = pd.DataFrame()
stat_buy = pd.Series()
stat_sell = pd.Series()


def projectionLong():
    import Strategy
    df = Strategy.df
    long = Strategy.long
    tpLong = Strategy.tpLong

    # creation of 2 dataframes, with buys and tp buys
    dbuy = pd.DataFrame([item[1] for item in long], [item[0] for item in long])
    typeb = []
    for k in range(0, len(dbuy[0])):
        typeb.append('buy')
    dbuy['Type'] = typeb

    dtpbuy = pd.DataFrame([item[1] for item in tpLong], [item[0] for item in tpLong])
    typebtp = []
    for k in range(0, len(dtpbuy[0])):
        typebtp.append('tp buy')
    dtpbuy['Type'] = typebtp

    # concat dataframes, then organize by datetime index
    global projBuy
    projBuy = pd.concat([dbuy, dtpbuy])
    projBuy.dropna(inplace=True)
    projBuy.columns = ['Values', 'Type']
    projBuy.sort_index(inplace=True)

    # calculation of profit with fees, little trick with 0 in order to align buy and 0, tp buy and profit
    profit = [0]
    fees = 0

    for j in range(1, len(projBuy['Values'])):
        com = projBuy['Values'].iloc[j - 1] * 0.001
        fees += com

        if projBuy['Type'].iloc[j] == 'tp buy':
            profit.append(projBuy['Values'].iloc[j] - projBuy['Values'].iloc[j - 1] - com)
            profit.append(0)

    if len(projBuy['Values']) > len(profit):
        profit.append(0)

    elif len(projBuy['Values']) < len(profit):
        del profit[-1]

    projBuy['Profit'] = profit
    projBuy['Cum. Profit'] = projBuy['Profit'].cumsum()

    # few stats
    global stat_buy
    stat_buy['Net profit'] = round(sum(profit), 2)
    stat_buy['Total % profit'] = round((stat_buy['Net profit'] / df['Open'].mean()) * 100, 2)
    stat_buy['Win trade'] = projBuy[projBuy['Profit'] > 0]['Profit'].count()
    stat_buy['Lose trade'] = projBuy[projBuy['Profit'] < 0]['Profit'].count()
    stat_buy['Com. paid'] = round(fees, 2)

    return stat_buy['Net profit']


def projectionShort():
    # the exact same process for short
    import Strategy
    df = Strategy.df
    short = Strategy.short
    tpShort = Strategy.tpShort

    dsell = pd.DataFrame([item[1] for item in short], [item[0] for item in short])
    type = []
    for k in range(0, len(dsell[0])):
        type.append('sell')
    dsell['Type'] = type

    dtpsell = pd.DataFrame([item[1] for item in tpShort], [item[0] for item in tpShort])
    typestp = []
    for k in range(0, len(dtpsell[0])):
        typestp.append('tp sell')
    dtpsell['Type'] = typestp

    global projSell
    projSell = pd.concat([dsell, dtpsell])
    projSell.dropna(inplace=True)
    projSell.columns = ['Values', 'Type']
    projSell.sort_index(inplace=True)

    profits = [0]
    fee = 0

    for j in range(1, len(projSell['Values'])):
        coms = projSell['Values'].iloc[j - 1] * 0.001
        fee += coms

        if projSell['Type'].iloc[j] == 'tp sell':
            profits.append(projSell['Values'].iloc[j-1] - projSell['Values'].iloc[j] + coms)
            profits.append(0)

    if len(projSell['Values']) > len(profits):
        profits.append(0)

    elif len(projSell['Values']) < len(profits):
        del profits[-1]

    projSell['Profit'] = profits
    projSell['Cum. Profit'] = projSell['Profit'].cumsum()

    global stat_sell
    stat_sell['Net profit'] = round(sum(profits), 2)
    stat_sell['Total % profit'] = round((stat_sell['Net profit'] / df['Open'].mean()) * 100, 2)
    stat_sell['Win trade'] = projSell[projSell['Profit'] > 0]['Profit'].count()
    stat_sell['Lose trade'] = projSell[projSell['Profit'] < 0]['Profit'].count()
    stat_sell['Com. paid'] = round(fee, 2)

    return stat_sell['Net profit']


def results(df):
    l = projectionLong()
    s = projectionShort()

    # calculation of numbers of days + profit realized / day
    # then total profit

    total = round(l + s, 2)
    first_date = df.index[0]
    nb_days = (datetime.today() - first_date).days
    profit_day = round(total / nb_days, 2)
    profit_month = round((profit_day * 30.42) / df['Open'].mean() * 100, 2)
    # 30.42 = 365/12

    return profit_day, profit_month






