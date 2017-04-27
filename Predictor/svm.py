from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.externals import joblib
from sklearn import preprocessing
from pymongo import MongoClient
import numpy as np
import copy
import pymongo

# f = open('appleAnnual.csv', 'r')
# f.readline()

def train(stock, dataSet):
	def predictNew(stock, data):
		# Open price prediction
		oModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
		oModel.fit(np.array(data[:-1]), np.array([i[2] for i in data[1:]]))

		joblib.dump(oModel, 'SVMoModel'+stock)

		oPrice = oModel.predict([data[-1]])[0]

		# High, low process adn prediction
		for i in range(len(data)-1):
			data[i][2] = data[i+1][2]
		data[-1][2] = oPrice

		hModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
		hModel.fit(np.array(data[:-1]), np.array([i[0] for i in data[1:]]))
		lModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
		lModel.fit(np.array(data[:-1]), np.array([i[1] for i in data[1:]]))

		joblib.dump(hModel, 'SVMhModel'+stock)
		joblib.dump(lModel, 'SVMlModel'+stock)

		hlPrice = [hModel.predict([data[-1]])[0], lModel.predict([data[-1]])[0]]

		# Volume
		for i in range(len(data)-1):
			data[i][0] = data[i+1][0]
			data[i][1] = data[i+1][1]
		data[-1][0] = hlPrice[0]
		data[-1][1] = hlPrice[1]

		vModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
		vModel.fit(np.array(data[:-1]), np.array([i[4] for i in data[1:]]))

		joblib.dump(vModel, 'SVMvModel'+stock)

		volume = int(vModel.predict([data[-1]])[0])

		# Close
		for i in range(len(data)-1):
			data[i][4] = data[i+1][4]
		data[-1][4] = volume

		cModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
		cModel.fit(np.array(data[:-1]), np.array([i[3] for i in data[1:]]))

		joblib.dump(cModel, 'SVMcModel'+stock)

		cPrice = cModel.predict([data[-1]])[0]

		new = [hlPrice[0], hlPrice[1], oPrice, cPrice, int(volume)]
		new = scaler.inverse_transform([new]).tolist()[0]
		print new
		return new

	# dataSet = []
	# for i in f.readlines():
	# 	i = i.split(',')
	# 	x = [float(j) for j in i[1:-1]]
	# 	x.append(int(i[-1]))
	# 	dataSet.append(x)
	# dataSet.reverse()
	dataSet = dataSet[:-20]

	scaler = preprocessing.RobustScaler()
	# scaler.scale_ = [1,1,1,1,0.1]
	dataSet = scaler.fit_transform(dataSet).tolist()
	joblib.dump(scaler, stock+'normalizeModel')

	for i in range(1):
		mData = copy.deepcopy(dataSet)
		temp = predictNew(stock, mData)
		dataSet.append(scaler.transform([temp])[0])

stockList = ['YHOO', 'GOOG', 'AAPL', 'CCF', 'BAC', 'FB', 'TWTR', 'BIDU', 'BABA', 'EDU']
dbClient = MongoClient()
db = dbClient.StockAnnual
for s in stockList:
	data = list(db[s].find().sort([('date', pymongo.ASCENDING)]))
	temp = []
	for i in data:
		i = [i['high'], i['low'], i['open'], i['close'], i['volume']]
		temp.append(i)
	train(s, temp)	
