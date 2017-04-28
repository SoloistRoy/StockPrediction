from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.externals import joblib
from sklearn import preprocessing
import copy
import datetime
import time
import pymongo
from pymongo import MongoClient
from multiprocessing.pool import ThreadPool as Pool

class shortTerm():
	def __init__(self):
		self.client = MongoClient()
		self.clientdb = self.client.StockAnnual

	def shortTermPredictor(self):
		res = []
		stockList = ['YHOO', 'GOOG', 'AAPL', 'CCF', 'BAC', 'FB', 'TWTR', 'BIDU', 'BABA', 'EDU']
		pool = Pool(10)
		for stock in stockList:
			sLatest = list(self.clientdb[stock].find().sort([('time', pymongo.DESCENDING)]))[:3]
			print sLatest
			temp = pool.apply_async(self.multi, (stock, sLatest,))
			t = temp.get()
			print t
			res.append(t)
		return res

	def multi(self, stock, sLatest):
		# sScaler = joblib.load('G:\Python\Web\StockPrediction\Predictor/'+stock+'normalize')
		cModel = joblib.load('G:\Python\Web\StockPrediction\Predictor\classifier'+stock)
		sModel = joblib.load('G:\Python\Web\StockPrediction\Predictor\short'+stock)
		# sLatest = sScaler.transform(sLatest).tolist()
		print sLatest
		l = []
		for i in sLatest:
			i = [i['high'],i['low'],i['open'],i['close']]
			l.append(i)
		return {'name':stock, 'price':sModel.predict(i).tolist()[0], 'trend':cModel.predict(i).tolist()[0]}

class annualPredict():
	def  __init__(self):
		self.modelList = ['oModel', 'hlModel', 'vModel', 'cModel']
		self.scaler = None

	def load(self, stockName, period, latest, method = ''):
		if method == 'SVM':
			self.modelList = ['oModel', 'hModel', 'lModel', 'vModel', 'cModel']
		# self.scaler = joblib.load('G:\Python\Web\StockPrediction\Predictor/'+stockName+'normalizeModel')
		self.scaler = joblib.load('/Users/jingyuan/WorkSpace/SEProject/StockPrediction/Predictor/'+stockName+'normalizeModel')
		for i in self.modelList:
			# model = joblib.load('G:\Python\Web\StockPrediction\Predictor/'+method+i+stockName)
			model = joblib.load('/Users/jingyuan/WorkSpace/SEProject/StockPrediction/Predictor/'+method+i+stockName)

			setattr(self, i, model)
			# print type(i)
		latest = self.scaler.transform(latest).tolist()
		return self.compute(period, latest, method)
		# print self.oModel.predict([[130,127,127,128,1000000]])

	def compute(self, period, latest, method):
		preResult = []
		next_days = []
		day = int(time.strftime("%d"))
		month = int(time.strftime("%m"))
		year = int(time.strftime("%Y"))
		d = datetime.date(year, month, day)
		for i in range(period):
			temp = copy.deepcopy(latest)
			print latest[-1]
			oPrice = self.oModel.predict(latest)

			for i in range(len(latest)-1):
				latest[i][2] = latest[i+1][2]
			latest[-1][2] = oPrice[0]
			if method == 'SVM':
				hlPrice = [self.hModel.predict(latest)[0], self.lModel.predict(latest)[0]]
			else:
				hlPrice = self.hlModel.predict(latest)
				hlPrice = hlPrice[0]

			for i in range(len(latest)-1):
				latest[i][0] = latest[i+1][0]
				latest[i][1] = latest[i+1][1]
			latest[-1][0] = hlPrice[0]
			latest[-1][1] = hlPrice[1]
			volume = self.vModel.predict(latest)

			for i in range(len(latest)-1):
				latest[i][4] = latest[i+1][4]
			latest[-1][4] = volume[0]
			cPrice = self.cModel.predict(latest)

			# next_days.append(self.next_weekday(d))
			d = self.next_weekday(d)

			latest = temp
			latest.pop(0)
			latest.append([hlPrice[0], hlPrice[1], oPrice[0], cPrice[0], int(volume[0])])
			tempRes = latest[-1]
			for i in tempRes:
				if i < 0:
					tempRes[tempRes.index(i)] = abs(i)
			tempRes = self.scaler.inverse_transform([tempRes]).tolist()[0]
			preResult.append(tempRes)
			preResult.append(str(self.next_weekday(d)))
		print preResult
		return preResult	
	
	def next_weekday(self, d):
		days = d.weekday() + 1 # tomorrow
		if days == 5: # today is Friday
			return d + datetime.timedelta(3)
		elif days == 6: # today is Saturday
			return d + datetime.timedelta(2)
		else:
			return d + datetime.timedelta(1)

	def next_weekdays(self, period): # next n week days
		next_days = []
		day = int(time.strftime("%d"))
		month = int(time.strftime("%m"))
		year = int(time.strftime("%Y"))
		d = datetime.date(year, month, day)
		for i in range(period):
			next_days.append(self.next_weekday(d))
			d = self.next_weekday(d)
		return next_days