
#all comments are about elements below the comment
import http.client
import urllib.request, urllib.parse, urllib.error
import json
import hashlib
import hmac
import time

class trade_api:
    __api_key	 = '';
    __api_secret	 = '';
    __nonce_v	 = 1;
    __wait_for_nonce = False
#init is the constructor for the class, so when you call the class these are the variables you will need
    def __init__(self, api_key, api_secret, wait_for_nonce=False):
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__wait_for_nonce = wait_for_nonce
#btc-e requires a constant ping with number that is changing i set ours to a formula with time
    def __nonce(self):
        if self.__wait_for_nonce: time.sleep(1)
        self.__nonce_v = str(time.time()).split('.')[0]
#this is the handshake for the keys to the api so btc-e knows its us
    def __signature(self, params):
        sig = hmac.new(self.__api_secret.encode(), params.encode(), hashlib.sha512)
        return sig.hexdigest()
#this the function that reaches out to the server with all the variables and requests information along with the sending the signature
    def __api_call(self, method, params):
        self.__nonce()
        params['method'] = method
        params['nonce'] = str(self.__nonce_v)
        params = urllib.parse.urlencode(params)
        headers = {"Content-type" : "application/x-www-form-urlencoded",
                    "Key" : self.__api_key,
		              "Sign" : self.__signature(params)}
        conn = http.client.HTTPSConnection("btc-e.com")
        conn.request("POST", "/tapi", params, headers)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        print (data)
        conn.close()
        return data
  #all requests for information need to be json, which is a form a encoding, this is where the encoding and request takes place 
    def get_param(self, couple, param):
        conn = http.client.HTTPSConnection("btc-e.com")
        conn.request("GET", "/api/2/" + couple + "/" + param)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        conn.close()
        return data
 #so btce has a 'getinfo' request that returns basice market info
    def getInfo(self):
        return self.__api_call('getInfo', {})
 
    def TradeHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
        params = {
            "from"	: tfrom,
            "count"	: tcount,
            "from_id"	: tfrom_id,
            "end_id"	: tend_id,
            "order"	: torder,
            "since"	: tsince,
            "end"	: tend,
            "pair"	: tpair}
        return self.__api_call('TradeHistory', params)
 #request function to see active orders
    def ActiveOrders(self, tpair):
        params = { "pair" : tpair }
        return self.__api_call('ActiveOrders', params)
#request to execute a trade, to make an order these variables need to be filled
    def Trade(self,ppair,ttype,rrate,aamount):
        params = {
            "pair"	: ppair,
            "type"	: ttype,
            "rate"	: rrate,
            "amount": aamount}
        return self.__api_call('Trade', params)
  #request to cancel order
    def CancelOrder(self, torder_id):
        params = { "order_id" : torder_id }
        return self.__api_call('CancelOrder', params)


#this is how you call functions from this class, you first need to initiate the class by binding it to a variable in this case "trade_api" and then you call "trade_api.function" which would be the same as saying "class.function(constructor variables)"
trade_api=trade_api('0KERY7J9-Y4D7A5OG-6MHDKJ58-9PFSYP1X-ZVBYETGC','0fad650c3b2a74bed850cd201648b44f03d152402ddec34fa742a855bfff1ad1')
#trade_api.Trade('btc_usd','sell',1000,0.01)
