from DBManager import get_stock_raw_data, get_stock_atrributes_data
import numpy as np
import matplotlib.pyplot as plt
import operator
import pandas as pd
def SMA(stock, N):
    # closingPrices, = get_stock_atrributes_data('AAPL', ['close'])
    print "SMA!!!!!!!!!!!!!!!!!!!!!!!!"
    return [np.mean(stock[i: i + N]) for i in range(len(stock) - N)]

def EMA(closingPrices, N):
    # closingPrices, = get_stock_atrributes_data(stock, ['close'])
    alpha = 2.0 / (N + 1)
    curEMA = closingPrices[0]
    res = [curEMA]
    for p in closingPrices[1:]:
        curEMA = (1 - alpha) * curEMA + alpha * p
        res.append(curEMA)
    return res

def RSI(prices, n = 14):
    # prices, = get_stock_atrributes_data(stock, ['close'])
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