from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import BayesianRidge
from sklearn.externals import joblib
from sklearn import preprocessing
from pymongo import MongoClient
import numpy as np
import copy
import pymongo

# f = open('appleAnnual.csv', 'r')
# f.readline()

def train(stock, dataSet):
	def predictNew(stock, data, label, plabel):
		# Open price prediction
		mlp = MLPClassifier(solver='lbfgs', activation='relu', verbose= False,max_iter='tol', hidden_layer_sizes=())
		mlp.fit(data, label)

		joblib.dump(mlp, 'classifier'+stock)

		bayes = BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, compute_score=False, copy_X=True, fit_intercept=True, lambda_1=1e-06, lambda_2=1e-06, n_iter=300, normalize=False, tol=0.001, verbose=False)
		bayes.fit(data, plabel)

		joblib.dump(bayes, 'short'+stock)


	# dataSet = []
	# for i in f.readlines():
	# 	i = i.split(',')
	# 	x = [float(j) for j in i[1:-1]]
	# 	x.append(int(i[-1]))
	# 	dataSet.append(x)
	# dataSet.reverse()
	dataSet = dataSet[-20:-5]

	scaler = preprocessing.RobustScaler()
	# scaler.scale_ = [1,1,1,1,0.1]
	# dataSet = scaler.fit_transform(dataSet).tolist()
	# joblib.dump(scaler, stock+'normalize')

	label, plabel = [], []
	for i in range(len(dataSet)-1):
		label.append(1 if dataSet[i] < dataSet[i+1] else 0)
		plabel.append(dataSet[i+1][2])

	for i in range(1):
		mData = copy.deepcopy(dataSet)
		predictNew(stock, mData[1:], label, plabel)
		# dataSet.append(scaler.transform([temp])[0])

stockList = ['YHOO', 'GOOG', 'AAPL', 'CCF', 'BAC', 'FB', 'TWTR', 'BIDU', 'BABA', 'EDU']
dbClient = MongoClient()
db = dbClient.StockAnnual
for s in stockList:
	data = list(db[s].find().sort([('date', pymongo.ASCENDING)]))
	temp = []
	for i in data:
		i = [i['high'], i['low'], i['open'], i['close']]
		temp.append(i)
	train(s, temp)	
