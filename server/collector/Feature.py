from sklearn import preprocessing
from DBManager import get_stock_atrributes_data

def getDataWithLag(rawData, lag):
    # type: (list, int) -> list
    """
    This is use for transformaing 1-d day to list of data in different time lags
    :param rawData: must be 1d list, like prices from database
    :param lag: time lag
    :return: list of range of data
    """
    res = []
    for i in range(len(rawData) - lag):
        res.append(rawData[i: i + lag])
    return res

def scaleData(data):
    min_max_scaler = preprocessing.MinMaxScaler()
    scaleData = min_max_scaler.fit_transform(data).tolist()
    return scaleData

def closingPriceFeature(stock, lag, scaling = True):
    closingPrices, = get_stock_atrributes_data(stock, ['close'])
    if scaling:
        scalePrices = scaleData(closingPrices)
    feature = getDataWithLag(scalePrices, lag)
    return closingPrices, feature
def stockFeatures(stock, lag, scaling = True):
    closePrice, volume, openPrice, highPrice, lowPrice = get_stock_atrributes_data(stock, ['close', 'volume', 'open', 'high', 'low'])
    if scaling:
        closePrice = scaleData(closePrice)
        volume = scaleData(volume)
        openPrice = scaleData(openPrice)
        highPrice = scaleData(highPrice)
        lowPrice = scaleData(lowPrice)
    features = []
    for c, v, o, h, l in zip(closePrice, volume, openPrice, highPrice, lowPrice):
        features.append([c, v, o, h, l])
    features = getDataWithLag(features, lag)
    res = []
    for list in features:
        res.append([item for sublist in list for item in sublist])
    return closePrice, res
#print stockFeatures('YHOO', 5)