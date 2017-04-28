Stock Prediction:

Getting Started:
1. Simply use git command:

	git clone https://github.com/SoloistRoy/StockPrediction 

to clone the repository or download ZIP documents.

2. Install Python 2.7 and MongoDB

3. Install Python packages, direct to StockPrediction/server run command:

	pip install -r requirements.txt

4. Install front-end requirements, run:

	npm install

5. Restore data, direct to StockPrediction/Data, run command:

	mongorestore --drop --db StockAnnual dump/StockAnnual
	mongorestore --drop --db StockRealtime dump/StockRealtime

6. Start server, direct to project directory, run command:

	python index.py

7. Open local browser, enter url:

	http://localhost:5000
	 
	