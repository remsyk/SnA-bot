import http.client
import urllib
import json
from threading import Timer

class price_ticker: 
    count = 0
    lastPrice = 0     
    
    def getTicker(self):
        Timer(10.0, self.getTicker).start()
        conn = http.client.HTTPSConnection("btc-e.com")
        #makes a request to get the ticker info
        conn.request("GET", "/api/2/btc_usd/ticker")
        response = conn.getresponse()
        data = json.load(response)    
        self.printTickerData(data)
        conn.close()
#function for defining price change
    def priceChange(self,oldPrice, newPrice):
        change = newPrice - oldPrice
        if change < 0:
            return "{0:.3f}".format(change)
        elif change == 0:
            return "===="
        else:
            return "+" + "{0:.3f}".format(change)
        
    def printTickerData(self,data):
        global count
        global lastPrice
        data2=json.dumps(data)
        f = open('price_ticker_log.txt', 'a')
        f.write(data2+'\n')
        f.close()
        
        #this formats the data to be read and printed as needed
        #"self" in python is how you call a function or variable inside of the class the function is defined in
        self.printLastDelta(self.count, data)
        print ("| HIGH - " + str(data['ticker']['high'])),
        print ("| LOW - " + str(data['ticker']['low'])),
        print ("| AVG - " + str(data['ticker']['avg'])),
        print ("| VOL - " + str(data['ticker']['vol'])),
        print ("| VOL_CUR - " + str(data['ticker']['vol_cur'])),
        print ("| LAST - " + str(data['ticker']['last'])),
        print ("| BUY - " + str(data['ticker']['buy'])),
        print ("| SELL - " + str(data['ticker']['sell'])),
        print ("| run#" + str(self.count))
#counter for requests
        self.count += 1
        lastPrice = data['ticker']['last']

#function to make sure that the last price is still the highest because it might not be for us since we are only pulling info from btc-e
    def printLastDelta(self,count, data):
        if count == 0:
            print ("LAST - " + str(data['ticker']['last']) + "(====)"),
        else :
            print ("LAST - " + str(data['ticker']['last']) + "(" + self.priceChange(lastPrice, data['ticker']['last']) + ")"),

#this is how you call functions from this class, you first need to initiate the class by binding it to a variable in this case "t" and then you call "t.function" which would be the same as saying "class.function(variables)"
t=price_ticker()
t.getTicker()
