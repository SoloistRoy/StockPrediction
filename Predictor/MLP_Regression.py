from sklearn.neural_network import MLPRegressor
import numpy as np
from DBManager import get_stock_atrributes_data
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from Feature import closingPriceFeature, stockFeatures
from random import shuffle
import copy

def mlp_predict(days, stock='YHOO'):
    # Generate sample data
    lag = 5
    offset = 20
    closingPrices, stockFeature = stockFeatures(stock, lag)
    #set training dat size
    N = len(stockFeature) / 3 * 2
    #training data
    y = closingPrices[lag:(N + lag)]
    X = stockFeature[0: N]
    #test data
    Z = stockFeature[N + offset: (N + days + offset)]
    # Fit regression model hidden_layer_sizes
    mlp = MLPRegressor(solver='lbfgs', activation='identity', verbose= False,max_iter='tol', hidden_layer_sizes=(50,))
    mlp.fit(X, y)
    y_log = mlp.predict(Z)
    #print np.ndarray.tolist(y_log)
    a = [round(i, 3) for i in list(y_log)]
    ax = plt.subplot(111)
    pre = 10
    b1 = closingPrices[N + lag + offset - pre: N + lag + offset]
    b2 = closingPrices[N + lag + offset - pre: N + lag + offset]
    b1.extend(a)
    b2.extend(closingPrices[N + lag + offset: N + lag + days + offset])
    plt.plot(b1, label='Prediction ' + stock + " " +str(lag))
    plt.plot(b2, label='Origin ' + stock + ' ' +str(lag))

    plt.legend()
    plt.show()
    return a
def svm_predict(days=10,stock='YHOO'):
    # Generate sample data
    lag = 2
    offset = 20
    closingPrices, stockFeature = stockFeatures(stock, lag)
    # set training dat size
    N = len(stockFeature) / 3 * 2
    # training data
    y = closingPrices[lag:(N + lag)]
    X = stockFeature[0: N]
    # test data
    Z = stockFeature[N + offset: (N + days + offset)]
    # Fit regression model
    svr_rbf = SVR(kernel='rbf', C=1e2, gamma=0.018)
    y_rbf = svr_rbf.fit(X, y).predict(Z)

    a = [round(i, 3) for i in list(y_rbf)]
    ax = plt.subplot(111)
    pre = 10
    b1 = closingPrices[N + lag + offset - pre: N + lag + offset]
    b2 = closingPrices[N + lag + offset - pre: N + lag + offset]
    b1.extend(a)
    b2.extend(closingPrices[N + lag + offset: N + lag + days + offset])
    plt.plot(b1, label='Prediction ' + stock + " " + str(lag))
    plt.plot(b2, label='Origin ' + stock + ' ' + str(lag))

    plt.legend()
    plt.show()
    return a


stockList = ['YHOO', 'GOOG', 'AAPL', 'BIDU', 'BABA']
for stock in stockList:
        mlp_predict(50,stock)