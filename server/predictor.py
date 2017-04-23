from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.externals import joblib
import copy
import datetime
import time

class annualPredict():
	def  __init__(self):
		self.modelList = ['oModel', 'hlModel', 'vModel', 'cModel']

	def load(self, stockName, period, latest):
		for i in self.modelList:
			# model = joblib.load('G:\Python\Web\StockPrediction\Predictor/'+i+stockName)
			model = joblib.load('/Users/jingyuan/WorkSpace/SEProject/StockPrediction/Predictor/'+i+stockName)
			setattr(self, i, model)
			# print type(i)
		return self.compute(period, latest)
		# print self.oModel.predict([[130,127,127,128,1000000]])

	def compute(self, period, latest):
		print period
		preResult = []
		next_days = []
		day = int(time.strftime("%d"))
		month = int(time.strftime("%m"))
		year = int(time.strftime("%Y"))
		d = datetime.date(year, month, day)
		for i in range(period):
			print latest
			oPrice = self.oModel.predict([latest])

			latest.append(oPrice[0])
			hlPrice = self.hlModel.predict([latest])

			latest.append(hlPrice[0][0])
			latest.append(hlPrice[0][1])
			volume = self.vModel.predict([latest])

			latest.append(volume[0])
			cPrice = self.cModel.predict([latest])

			# next_days.append(self.next_weekday(d))
			d = self.next_weekday(d)

			latest=[float(hlPrice[0][0]), float(hlPrice[0][1]), float(oPrice[0]), float(cPrice[0]), int(volume[0])]
			preResult.append(copy.deepcopy(latest))
			preResult.append(str(self.next_weekday(d)))
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