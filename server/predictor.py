from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.externals import joblib
import copy

class annualPredict():
	def  __init__(self):
		self.modelList = ['oModel', 'hlModel', 'vModel', 'cModel']

	def load(self, stockName, period, latest):
		for i in self.modelList:
			model = joblib.load('G:\Python\Web\StockPrediction\Predictor/'+i+stockName)
			setattr(self, i, model)
			# print type(i)
		return self.compute(period, latest)
		# print self.oModel.predict([[130,127,127,128,1000000]])

	def compute(self, period, latest):
		preResult = []
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

			latest=[float(hlPrice[0][0]), float(hlPrice[0][1]), float(oPrice[0]), float(cPrice[0]), int(volume[0])]
			preResult.append(copy.deepcopy(latest))
		return preResult	