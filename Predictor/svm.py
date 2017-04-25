from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.externals import joblib
from sklearn import preprocessing
import numpy as np
import copy

f = open('appleAnnual.csv', 'r')
f.readline()

def predictNew(data):
	# Open price prediction
	oModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
	oModel.fit(np.array(data[:-1]), np.array([i[2] for i in data[1:]]))

	joblib.dump(oModel, 'SVMoModelAAPL')

	oPrice = oModel.predict([data[-1]])[0]

	# High, low process adn prediction
	for i in range(len(data)-1):
		data[i].append(data[i+1][2])
	data[-1].append(oPrice)

	hModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
	hModel.fit(np.array(data[:-1]), np.array([i[0] for i in data[1:]]))
	lModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
	lModel.fit(np.array(data[:-1]), np.array([i[1] for i in data[1:]]))

	joblib.dump(hModel, 'SVMhModelAAPL')
	joblib.dump(lModel, 'SVMlModelAAPL')

	hlPrice = [hModel.predict([data[-1]])[0], lModel.predict([data[-1]])[0]]

	# Volume
	for i in range(len(data)-1):
		data[i].append(data[i+1][0])
		data[i].append(data[i+1][1])
	data[-1].append(hlPrice[0])
	data[-1].append(hlPrice[1])

	vModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
	vModel.fit(np.array(data[:-1]), np.array([i[4] for i in data[1:]]))

	joblib.dump(vModel, 'SVMvModelAAPL')
	print 'input: ',data[-1]

	volume = int(vModel.predict([data[-1]])[0])

	# Close
	for i in range(len(data)-1):
		data[i].append(data[i+1][4])
	data[-1].append(volume)

	cModel = SVR(kernel='rbf', C=1e2, gamma=0.018)
	cModel.fit(np.array(data[:-1]), np.array([i[3] for i in data[1:]]))

	joblib.dump(cModel, 'SVMcModelAAPL')
	print 'input: ',data[-1]

	cPrice = cModel.predict([data[-1]])[0]

	new = [hlPrice[0], hlPrice[1], oPrice, cPrice, volume]
	new = scaler.inverse_transform([new]).tolist()[0]
	print new
	return new

dataSet = []
for i in f.readlines():
	i = i.split(',')
	x = [float(j) for j in i[1:-1]]
	x.append(int(i[-1]))
	dataSet.append(x)
dataSet.reverse()

scaler = preprocessing.MinMaxScaler()
dataSet = scaler.fit_transform(dataSet).tolist()
joblib.dump(scaler, 'normalizeModel')

for i in range(1):
	mData = copy.deepcopy(dataSet)
	temp = predictNew(mData)
	dataSet.append(temp)