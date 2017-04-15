from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.externals import joblib

class annualPredict():
	def  __init__(self):
		self.modelList = ['oModel', 'hlModel', 'vModel', 'cModel']

	def load(self, stockName):
		for i in self.modelList:
			model = joblib.load(i+stockName) 

	def compute(self):
		for i in self.modelList:
