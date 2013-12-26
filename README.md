forex-backtester-python
=======================

An application to backtest basic trading strategies for the FX market, based on historical data.

This code is written for Python 2.7, and is not compatible with Python 3. Prerequisites: Tkinter

To run the program, download all the files, maintain the same directory structure, and run the input_handling.py file from the Python interpreter. The parameter settings are as follows:

Start/End Date: the dates that bound the historical data that is going to be tested
Initial Deposit: the amount of money (USD) in the brokerage account to begin with
TimeFrame: the width of each bar of the historical data that is going to be tested; this is the timeframe used for each strategy
Symbol: support for only EURUSD, USDJPY, GBPUSD, and USDCHF with included data
Position to Trade: restrict the backtest to include only long positions, short positions, or both
Trading Criterium: the main strategy used to simulate historical trades (Moving Average Crossover and Stochastics included)
Leverage (margin): the max leverage ratio permissible
Preferred Lot Size: a fixed lot size to be traded when a position is opened. If free margin constrains the lot size to be less, it will be adjusted during the test.
Spread Modeling Technique: Average Spreads - assume that spreads stay constant throughout the historical data
Trade Management Technique:
  TP/SL - set a fixed take profit and stop loss level in pips from entry price
  Price % SL - set the stop loss to be a percentage of price and update every bar

Once these parameters are entered, the program will run a rudimentary backtest using bar by bar analysis to determine what the final account balance will be.

This program can be extended by adding more trading strategies. They should implement the same interface as the Moving Average and Stochastic strategies.
