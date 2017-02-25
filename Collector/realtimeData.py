import datetime
import time as T

from yahoo_finance import Share

# find the date of yesterday
now = datetime.datetime.now()

# get the records ranging from max date in DB to yesterday
BeginTime = now.replace(hour=9, minute=0, second=0, microsecond=0)
EndTime = now.replace(hour=16, minute=0, second=0, microsecond=0)
# LocalTime = T.strftime('%Y-%m-%d ',T.localtime(T.time()))
# while now > BeginTime and now < EndTime:
while 1:
    now = datetime.datetime.now()
    StockList = ['YHOO', 'GOOG']
    for stock in StockList:
        Symbol = stock
        Company = Share(stock)
        Company.refresh()
        Price = Company.get_price()
        Time = Company.get_trade_datetime()
        Volume = Company.get_volume()
        purchases = (Symbol, Price, Time, Volume)
        print purchases
    T.sleep(5)
