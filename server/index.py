from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo

# app = Flask('StockAnnual', template_folder = 'G:\Python\Web\StockPrediction',static_folder='G:\Python\Web\StockPrediction')
app = Flask('StockAnnual', template_folder = '/Users/jingyuan/WorkSpace/SEProject/StockPrediction',static_folder='/Users/jingyuan/WorkSpace/SEProject/StockPrediction')
app.config['MONGO_DBNAME'] = 'StockAnnual'
app.config['MONGO_URI'] = 'mongodb://localhost/StockAnnual'
app.config['SECRET_KEY'] = 'super secret key'

mongo = PyMongo(app)
# dbClient = MongoClient()
# db = dbClient.StockRealtime

@app.route('/')
def index():
	if 'piece' in session:
		m = session['piece']
		session.clear()
		return str(m)

	# online_users = mongo.db.GOOG.find({'date': '2017-02-01'})
	return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
	# stockName = request.form['stockName']
	print(request.json)
	stockName = request.json['stockName']
	stock = mongo.db[stockName]
	m = stock.find({})
	session['piece'] = m[0][u'high']
	# return redirect(url_for('index'))
	return str(m[4][u'high'])

if __name__ == '__main__':
	app.debug = True
	app.run()