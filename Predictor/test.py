from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
import numpy as np
import copy

def method(alpha):
	return Lasso(alpha)

f = open('appleAnnual.csv', 'r')
f.readline()

def predictNew(data):
	# Open price prediction
	oModel = Lasso(0.04)
	oModel.fit(np.array(data[:-1]), np.array([i[2] for i in data[1:]]))
	oPrice = oModel.predict([data[-1]])[0]

	# High, low process adn prediction
	for i in range(len(data)-1):
		data[i].append(data[i+1][2])
	data[-1].append(oPrice)

	hlModel = Lasso(1.5)
	hlModel.fit(np.array(data[:-1]), np.array([i[0:2] for i in data[1:]]))
	hlPrice = hlModel.predict([data[-1]])[0]

	# Volume
	for i in range(len(data)-1):
		data[i].append(data[i+1][0])
		data[i].append(data[i+1][1])
	data[-1].append(hlPrice[0])
	data[-1].append(hlPrice[1])

	vModel = Ridge(0.01)
	vModel.fit(np.array(data[:-1]), np.array([i[4] for i in data[1:]]))
	volume = int(vModel.predict([data[-1]])[0])

	# Close
	for i in range(len(data)-1):
		data[i].append(data[i+1][4])
	data[-1].append(volume)

	cModel = Ridge(1)
	cModel.fit(np.array(data[:-1]), np.array([i[3] for i in data[1:]]))
	cPrice = cModel.predict([data[-1]])[0]

	new = [hlPrice[0], hlPrice[1], oPrice, cPrice, volume]
	print new
	return new

dataSet = []
for i in f.readlines():
	i = i.split(',')
	x = [float(j) for j in i[1:-1]]
	x.append(int(i[-1]))
	dataSet.append(x)
dataSet.reverse()

for i in range(10):
	mData = copy.deepcopy(dataSet)
	temp = predictNew(mData)
	dataSet.append(temp)