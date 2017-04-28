import urllib
import time
import json
from urllib import urlopen
def get_quote(stockList):
    concatSymbol = ','.join(stockList)
    basic_url = 'http://finance.google.com/finance/info?q='
    print basic_url + concatSymbol
    content = urlopen(basic_url + concatSymbol).read()
    obj = json.loads(content[3:])
    # for sInfo in obj:
    #     print sInfo
    parsed_data = [float(sInfo['l_cur']) for sInfo in obj]
    #print parsed_data
    return parsed_data

# timeout = 1000
# while 1:
#     stockList = ['YHOO', 'GOOGL', 'AAPL', 'NYSEMKT:CCF', 'BAC', 'FB', 'TWTR', 'BIDU', 'BABA', 'EDU']
#     quote = get_quote(stockList)
#     print quote
#     time.sleep(timeout)


