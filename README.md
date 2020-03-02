# WH-Bot
A python cryptocurrencies trading bot.


This program aims to trade in the crypto markets 24/7 and can be used as a support for several strategies, timeframes, pairs. 
Education purpose only, use it under your own risks.

To run this script, you'll need few packages : pandas, numpy, mplfinance, schedule, yfinance, ccxt, datetime, time, warnings.
To download them, open your command prompt and type : pip install package_name (e.g. pip install pandas).

For the purpose of the script, we use a simple moving average (SMA) strategy: 
go long when SMA > Previous SMA and go short when SMA < Previous SMA.
Details in Strategy.py (main file).

First, need a backtest strategy in order to verify historical behaviour, 
refer to Strategy.py and Backtest.py files. 
Then, if validated enter in real time trading, refer to Live.py file.

To get input trading data, there are two ways:
- Yahoo! Finance: not required to login, simplest way and use by default in Strategy.py,
	only usable with one day timeframe and historical strategy
- CCXT: requires broker account with API keys, only for advanced users,
	the ones supported by ccxt are visible here : 
	https://github.com/ccxt/ccxt#supported-cryptocurrency-exchange-markets.
	Use ccxt with Live.py, need data in real time (not available with yahoo finance).
	To use ccxt in Strategy.py, remove '#' of lines 12 to 14 and add '#' line 10
	in order to use Dataframe.py, file including ccxt data.

When all above downloaded, execute Strategy.py.
Script will execute backtest including chart and will show strategy result:
- Net backtest period profit $
- Total % profit backtest period
- Number of winning and losing trades
- Commission paid
- Daily profit $
- Monthly profit %

To modify the strategy, use your own applicable indicators and update Indicators.py accordingly.
Then update Strategy.py lines 38 to 85 with your own study.

To modify pairs, modify Strategy.py line 10 with your choosen pair.
To modify timeframe (ccxt only), modify Dataframe.py line 12 with your choosen period.

Enjoy!
