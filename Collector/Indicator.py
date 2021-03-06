from DBManager import get_stock_raw_data, get_stock_atrributes_data
import numpy as np
import matplotlib.pyplot as plt
import operator
import pandas as pd
import datetime
from flask_pymongo import PyMongo
import pymongo
def SMA(stockName, dateRange, N):
    # Calculate date range
    stock = mongo.db[stockName]
    dtsmall = datetime.datetime(int(dateRange[6:10]),int(dateRange[:2]),int(dateRange[3:5]))
    dtlarge = datetime.datetime(int(dateRange[19:]),int(dateRange[13:15]),int(dateRange[16:18]))
    print dtlarge,dtsmall
    indResult = []
    indData = stock.find({'date':{'$gte':dtsmall, '$lte':dtlarge}}).sort([('date', pymongo.ASCENDING)])
	# Get close price list (indResult)
    for i in indData:
		temp = float(i['close'])
		indResult.append(temp)
    # closingPrices  = []
    # closingPrices, = get_stock_atrributes_data(stockName, ['close'])
    # return [np.mean(closingPrices[i: i + N]) for i in range(len(closingPrices) - N)]
    print "=================SMA!!!!!!!!!!!!!!!!"
    return [np.mean(stock[i: i + N]) for i in range(len(stock) - N)]

def EMA(stock, N):
    closingPrices, = get_stock_atrributes_data(stock, ['close'])
    alpha = 2.0 / (N + 1)
    curEMA = closingPrices[0]
    res = [curEMA]
    for p in closingPrices[1:]:
        curEMA = (1 - alpha) * curEMA + alpha * p
        res.append(curEMA)
    return res
def RSI(stock, n = 14):
    prices, = get_stock_atrributes_data(stock, ['close'])
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi[n:]
def MACD(stock, slow = 26, fast = 12):
    emaSlow = EMA(stock, slow)
    emaFast = EMA(stock, fast)
    return emaSlow, emaFast
def test(stock):
    ax = plt.subplot(111)
    closingPrices, = get_stock_atrributes_data(stock, ['close'])
    plt.plot(closingPrices, label = 'close price')
    plt.plot(EMA(stock, 10), label = 'EMA')
    plt.plot(SMA(stock, 10), label = 'SMA')
    plt.plot(RSI(stock), label = 'RSI')
    plt.legend()
    plt.show()
    #print map(operator.sub, closingPrices, EMA(stock, 10))
    #print len(EMA(stock, 10))
def test_EMA(stock):
    ax = plt.subplot(111)
    closingPrices, = get_stock_atrributes_data(stock, ['close'])
    plt.plot(closingPrices, label='close price')
    plt.plot(EMA(stock, 10), label='EMA_10')
    plt.plot(EMA(stock, 20), label='EMA_20')
    plt.plot(EMA(stock, 100), label='EMA_100')
    plt.legend()
    plt.show()
def test_MACD(stock):
    ax = plt.subplot(111)
    closingPrices, = get_stock_atrributes_data(stock, ['close'])
    plt.plot(closingPrices, label='close price')
    eS, eF = MACD(stock)
    plt.plot(eS, label='slow')
    plt.plot(eF, label='fast')
    plt.legend()
    plt.show()
# test_MACD('YHOO')
# test_EMA('YHOO')
# test('YHOO')
dateRange = '02/01/2016 - 02/01/2017'
plt.plot(SMA('YHOO',dateRange,10), label = 'SMA')