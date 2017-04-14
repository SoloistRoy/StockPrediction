from sklearn.neural_network import MLPClassifier
import numpy as np
from DBManager import get_stock_atrributes_data
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn import  preprocessing
from Feature import closingPriceFeature, stockFeatures
def mlp_predict(days, stock='YHOO'):
    # Generate sample data
    lag = 5
    offset = 0
    closingPrices, stockFeature = stockFeatures(stock, lag)
    N = len(stockFeature) / 3 * 2
    upDown = []
    for i in range(1, len(closingPrices)):
        upDown.append(-1 if (closingPrices[i - 1] > closingPrices[i]) else 0)
    trainLable = upDown[lag - 1:(N + lag - 1)]
    trainData = stockFeature[0: N]
    testData = stockFeature[N + offset: (N + days + offset)]
    testLable = upDown[N + lag + offset - 1: N + lag + days + offset - 1]
    # Fit model
    mlp = MLPClassifier(solver='lbfgs', activation='relu', verbose= False,max_iter='tol', hidden_layer_sizes=())
    mlp.fit(trainData, trainLable)
    y_pre = mlp.predict(testData).tolist()
    print mlp.score(testData,testLable)

    return y_pre
def svm_predict(days=10,stock='YHOO'):
    # Generate sample data
    lag = 10
    closingPrices, stockFeature = stockFeatures(stock, lag)
    N = len(stockFeature) /2
    y = closingPrices[lag:(N + lag)]

    X = stockFeature[0: N]
    Z = stockFeature[N: (N + days)]
    # Fit regression model
    svr_rbf = SVR(kernel='rbf', C=1e2, gamma=0.018)
    y_rbf = svr_rbf.fit(X, y).predict(Z)

    a = [round(i, 3) for i in list(y_rbf)]
    ax = plt.subplot(111)
    plt.plot(a, label='Prediction ' + stock + " " +str(lag))
    plt.plot(closingPrices[N + lag: N + lag + days], label='Origin ' + stock + ' ' +str(lag))
    plt.legend()
    plt.show()
    return a


stockList = ['YHOO', 'GOOG', 'AAPL', 'BIDU', 'BABA']
for stock in stockList:
    mlp_predict(50,stock)