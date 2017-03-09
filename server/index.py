from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from flask import render_template

app = Flask('StockAnnual', template_folder = 'G:\Python\Web\StockPrediction',static_folder='G:\Python\Web\StockPrediction')
# app = Flask('StockAnnual', template_folder = '')

mongo = PyMongo(app)
# dbClient = MongoClient()
# db = dbClient.StockRealtime

@app.route('/')
def hello_world():
	# online_users = db.GOOG.find({'date': '2017-02-01'})
	online_users = mongo.db.GOOG.find({'date': '2017-02-01'})
	return render_template('index.html', online_users=online_users)
	# return type(online_users)
    # return 'Hello World!'

if __name__ == '__main__':
	app.debug = True
	app.run()