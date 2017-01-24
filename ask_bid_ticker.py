'''
Created on Jan 2, 2017

@author: i77ki
'''
import http.client
import urllib
import json
from threading import Timer


class ask_bid_ticker:

    def __init__(self,aprice,aamount,bprice,bamount):
            self.aamount = []
            self.bprice = []
            self.bamount = []
            self.aprice = []

    def getDepth(self):
        Timer(10.0, self.getDepth)
        conn = http.client.HTTPSConnection("btc-e.com")
        #makes a request to get the ask bid info called "depth"
        conn.request('GET','https://btc-e.com/api/3/depth/btc_usd')
        response = conn.getresponse()
        data = json.load(response)    
        #self.ask_output(data)
        #self.bid_output(data)
        conn.close()
        return data

    def ask_output(self,data):
        depth=json.dumps(data)
        sep='bids": ['
        sep2='asks": ['
        asks=depth.split(sep,1)[0]
        asks=''.join(depth.split(sep2)[1:]) 
        asks=asks.replace("], ","\n")
        asks=asks.replace("[","")
        asks=asks.replace(" ","")
        asks=asks.strip("]}")
        return asks
    
    def bid_output(self,data):
        depth=json.dumps(data)
        sep='bids": ['
        sep2='asks": ['
        bids=''.join(depth.split(sep)[1:])
        bids=bids.replace("], ","\n")
        bids=bids.replace("[","")
        bids=bids.replace(" ","")
        bids=bids.strip("]}")
        return bids
    
    def bid_amount(self):
        Timer(10.0, self.bid_amount)
        bids=list(self.bid_output(self.getDepth()).splitlines())
        for l in bids:
            row = l.split(',')
            self.bamount.append(row[1])
        return self.bamount
    
    def bid_price(self):
        Timer(10.0, self.bid_price)
        bids=list(self.bid_output(self.getDepth()).splitlines())
        bprice = []
        for l in bids:
            row = l.split(',')
            self.bprice.append(row[0])
        return self.bprice
    
    def ask_amount(self):
        Timer(10.0, self.ask_amount).start()
        asks=list(self.ask_output(self.getDepth()).splitlines())
        for l in asks:
            row = l.split(',')
            self.aamount.append(row[1])
        return self.aamount
    
    def ask_price(self):
        Timer(10.0, self.ask_price)
        asks=list(self.ask_output(self.getDepth()).splitlines())
        for l in asks:
            row = l.split(',')
            self.aprice.append(row[0])
        return self.aprice


