'''
Created on Jan 2, 2017

@author: i77ki
'''
import http.client
import urllib
import json
from threading import Timer


class ask_bid_ticker:
    
    def getDepth(self):
        Timer(10.0, self.getDepth).start()
        conn = http.client.HTTPSConnection("btc-e.com")
        #makes a request to get the ask bid info called "depth"
        conn.request('GET','https://btc-e.com/api/3/depth/btc_usd')
        response = conn.getresponse()
        data = json.load(response)    
        self.printDepthData(data)
        conn.close()
   
    def printDepthData(self,data):
        depth=json.dumps(data)
        #all of this below was my halfass way of formatting the ask bid information as it comes in, basically just split it up by parsing it and setting delimiters
        sep='bids": ['
        sep2='asks": ['
        asks=depth.split(sep,1)[0]
        asks=''.join(depth.split(sep2)[1:]) 
        asks=asks.replace("], ","\n")
        asks=asks.replace("[","")
        asks=asks.replace(" ","")
        asks=asks.strip("]}")
        bids=''.join(depth.split(sep)[1:])
        bids=bids.replace("], ","\n")
        bids=bids.replace("[","")
        bids=bids.replace(" ","")
        bids=bids.strip("]}")
        
#this opens 2 files, one for bids and one for asks and the writes the info into them
        a = open('asks.txt', 'a')
        b=open('bids.txt','a')
        a.write(asks+'\n')
        b.write(bids+'\n')
        a.close()
        b.close()

t=ask_bid_ticker()
t.getDepth()
