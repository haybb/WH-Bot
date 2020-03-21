# WH-Bot
A python trading bot.

### Goal
This program aims to **trade in all available markets 24/7** and can be used as a support for several *strategies, time frames, pairs*. 
Education purpose only, use it under your own risks.

### For running the script
Need few packages : *pandas, numpy, mplfinance, schedule, yfinance, ccxt, datetime, time, warnings.*
To download them, open your command prompt, navigate to WH-Bot folder (after having downloaded this program),
and type : ```pip install -r requirements.txt```
or do it manually by typing : ```pip install package_name``` (e.g. ```pip install pandas```)

### Execution
Just have to launch `WH-Bot.exe`.
Or you can also execute `Main.py`.

![Screen](https://user-images.githubusercontent.com/61158178/77209752-61e7b000-6aff-11ea-8c2d-a08c372144b3.PNG)

### Strategy
For the purpose of the script, we use a Simple Moving Average (SMA) strategy: 
go long when SMA > Previous SMA and go short when SMA < Previous SMA.
Details in ```Strategy.py```.

### Functioning
First, need a backtest strategy in order to verify historical behaviour, 
refer to ```Strategy.py``` and ```Backtest.py``` files. 
Then, if validated enter in real time trading, refer to ```Live.py``` file.

### To get input trading data
- **Yahoo Finance:** not required to login, simplest way and use by default in ``Strategy.py``,
	only usable with historical strategy.
- **CCXT:** requires broker account with API keys, _only for advanced users,_
	(the ones supported by ccxt are visible [here](https://github.com/ccxt/ccxt#supported-cryptocurrency-exchange-markets))
	Use ccxt with `Live.py`, need data in real time (not available with Yahoo Finance).

### Execution
When all above downloaded, execute ```Main.py``` or `WH-Bot.exe`.
Script will execute backtest and will show strategy results :
- Net backtest period profit $
- Total % profit backtest period
- Number of winning and losing trades
- Commission paid
- Daily profit $
- Monthly profit %
It also includes chart. It shows candlesticks with selected settings.

To modify the strategy, use your own applicable indicators and update ```Indicators.py``` accordingly.
Then update ```Strategy.py``` with your own study.
If everything's fine, update `Live.py` and you're ready to enter in the real trading world.

#### Feel free to contribute
#### Enjoy!
