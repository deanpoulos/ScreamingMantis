#=============================================================================#
#    Screaming Mantis: uses binance & kucoin APIs and prints relevant info    #
#=============================================================================#

import keys     # abstract away our keys so we don't compromise security
import datetime # not sure if necessary
from binance.client import Client as bCli   # from python-binance via pip
from kucoin.client  import Client as kCli   # from python-kucoin via pip
from time           import sleep            # to loop program and update 1m
import time

# formatting colours
GRN = '\033[00;92m';        BLU = '\033[94;01m'
ORG = '\033[38;5;215m';  RED = '\033[91m'
CLR = '\033[00;00m';        WHT = '\033[00;01m'

# kline fetching options (using dateparsing format)
start_str="3 min ago UTC"

# initialise our exchanges with our unique keys and static attributes
binance = { 'client':   bCli(keys.APIKey, keys.SecretKey),
            'name':     ORG + "[BINANCE]" + CLR,
            'pair':     "NEOETH"                           }
kucoin  = { 'client':   kCli(keys.APIKey, keys.SecretKey),
            'name':     BLU + "[KUCOIN]" + CLR,
            'pair':     "NEO-ETH"                           }
exchanges = (binance, kucoin)

# initialise more important dynamic data and relay
while 1:
    for exchange in exchanges:
        # account for some differences in API
        if exchange == binance:
            # get historical klines
            exchange["historicalKline"] = \
            exchange["client"].get_historical_klines(symbol=exchange["pair"], 
                interval='1m', start_str=start_str) # data from every minute
            # get symbol info
            exchange["status"] = \
            exchange["client"].get_symbol_info(exchange["pair"])["status"]
        elif exchange == kucoin:
            # get historical klines
            exchange["historicalKline"] = \
            exchange["client"].get_kline_data(exchange["pair"], 
            exchange["client"].RESOLUTION_1MINUTE, 
            int(time.time()) - int(start_str[0])*60, int(time.time()))
            # create pseudo symbol info
            exchange["status"] = \
            exchange["client"].get_tick(exchange["pair"])["trading"]
            exchange["status"] = int(exchange["status"])*"TRADING" + \
                                 (not int(exchange["status"]))*"INACTIVE"

    # format and print important client info
    for exchange in exchanges:
        # print name, exchange and status
        print("{0}Trading Pair: {1} {2}{3} {4}[{5}]".format(WHT, exchange["name"], 
            CLR, exchange["pair"], GRN, exchange["status"]))
        # print closing prices over interval
        print("{0} - Closing Prices: {1}".format(WHT, CLR))
        for list in exchange["historicalKline"]:
            if not (list[4] == None):
                print("     {0}{1} {2}[-{3} seconds]".format(CLR, list[4], 
                                   RED, int(time.time()) - int(list[0])/1000))
    
    # wait for a minute
    sleep(60)
