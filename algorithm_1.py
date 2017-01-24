'''
Created on Jan 12, 2017

@author: i77ki
'''
from threading import Timer
from ask_bid_ticker import  ask_bid_ticker
from trade_api import trade_api

r=trade_api('S4KOTSSQ-ZSFTSB76-4C7IM60G-SWSKTWUR-23GB0X2N','dbd6466fed11a6c81eb4fef7eaf84801cdf1b94736e4748f1a1b06adb1538461')
ap,aa,bp,ba=[],[],[],[]
t=ask_bid_ticker(ap,aa,bp,ba)

def ask_amount_max():
    while True:
        m=t.ask_amount().index(max(t.ask_amount()))
        if len(t.ask_amount())>100000:
            break
    return m

  
k=t.ask_price()
r.Trade('btc_usd', 'sell', k[ask_amount_max()]-1, 0.01)
