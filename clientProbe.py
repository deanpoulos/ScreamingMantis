# Agenda: =====================================================================#
# x add difference between closing prices on primitive example
# x add two more exchanges: Bitfinex & BTC Markets                             
# / add buy/sell order price comparison                                       
# - implement dynamic exchange information fetching for BTCMarkets & Bitfinex
# - implement price comparisons between BTCMarkets & Bitfinex

# library headers ============================================================#

import keys             # abstract away our keys so we improve security
import datetime;        import time                 # for system clock time
from formatting         import *                    # abstract away esc seqs
from binance.client     import Client     as bin    # from python-binance pip
from kucoin.client      import Client     as kuc    # from python-kucoin pip
from btcmarkets.api     import BTCMarkets as btc    # from BTCMarkets github
from bitfinex.client    import Client     as bit    # from bitfinex pip
from time               import sleep                # to loop program update 1m

# KuCoin & Binance ===========================================================#

def initialiseKuCoinBinance(exchanges, minutes, start_str):
    """
        initialises the dynamic data for exchanges Binance and KuCoin such as
        price action and trading status
    """

    # find status (active or inactive) and price data for two exchanges
    for exchange in exchanges:
        # account for some differences in API client
        if exchange == exchanges[BINANCE]:
            # get price history
            exchange["history"] = \
            exchange["client"].get_historical_klines(symbol=exchange["pair"], 
            interval='1m', start_str=start_str) # data from every minute
            # get status info
            exchange["status"] = \
            exchange["client"].get_symbol_info(exchange["pair"])["status"]
            exchange["status"] = \
            (int(not (exchange["status"].find("TRADING") == -1)) * ACTIVE) \
               + (int(exchange["status"].find("TRADING") == -1)  * INACTIVE)
        elif exchange == exchanges[KUCOIN]:
            # get price history
            exchange["history"] = \
            exchange["client"].get_kline_data(exchange["pair"], 
            exchange["client"].RESOLUTION_1MINUTE, 
            int(time.time()) - minutes*60, int(time.time()))
            # create status info
            exchange["status"] = \
            exchange["client"].get_tick(exchange["pair"])["trading"]
            exchange["status"] = \
                 int(exchange["status"]) * ACTIVE + \
            (not int(exchange["status"]))* INACTIVE

    for exchange in exchanges:
        exchange["closingPrices"] = []
        # grab closing price/age pairs
        for list in exchange["history"]:
            if not (list[4] == None):
                # calculate age of price using timestamps
                age = int(time.time()) - int(list[0])/1000

                # store this info in our exchange data structure
                exchange["closingPrices"].append({ age: list[4] })

    return exchanges



def printTickInfoKuCoinBinance(exchanges):
    """
        print contextual exchange/pair information for Binance and KuCoin
        and get prices
    """

    for exchange in exchanges:
        # print name, exchange and status
        print("{0}Trading Pair: {1} {2}{3} {4}".format(WHT, exchange["name"], 
            CLR, exchange["pair"], exchange["status"]))

        # print closing prices over interval
        print("{0} - Closing Prices: {1}".format(WHT, CLR))
        for dict in exchange["closingPrices"]:
            # iterate over dicts like a list
            dict = sum(dict.items(), ())
            # print price and age
            print("     {0}{1} {2}{3} s ago".format(CLR, dict[1], RED, dict[0]))



def closingDifferenceKuCoinBinance(exchanges):
    """
        calculate closing price difference between KuCoin and Binance 
    """

    # assert we have at least one entry for price action in kucion
    if (exchanges[KUCOIN]["closingPrices"] == []):
        print(NO_DATA)

    else:
        # for price/age entries in KuCoin
        for bidPrice in exchanges[KUCOIN]["closingPrices"]:
            # for all entries in Binance's price/age pair list
            for i in range(0,len(exchanges[BINANCE]["closingPrices"])):
                # get ages through keys
                bidPriceAge = bidPrice.keys()
                askPriceAge = exchanges[BINANCE]["closingPrices"][i].keys()
                # iterate until we find matching ages to compare
                # note next(iter(bidPriceAge)) = timesA[0] for a set
                if (next(iter(bidPriceAge)) == next(iter(askPriceAge))):
                    askPrice = exchanges[BINANCE]["closingPrices"][i]
                    break

            # calculate and print the difference in prices at a particular age
            age = next(iter(bidPrice))
            difference = ((bidPrice[age] - float(askPrice[age])) /\
                           bidPrice[age]) * 100

            print(("{0}Difference is {1}{2:.4f}% {3}from {4:.1f} " +
                   "minute(s) ago").format(WHT,YEL,difference,WHT,abs(age/60)))

# BTCMarkets & Bitfinex ======================================================#

def initialiseBTCMarketsBitfinex(exchanges):
    """
        initialises the dynamic data for exchanges Binance and KuCoin such as
        price action and trading status
    """

    for exchange in exchanges:

        if exchange == exchanges[BITFINEX]:
            # get price
            print(exchange["client"].ticker(exchange["pair"]))
            print(exchange["client"].today(exchange["pair"]))
            print(exchange["client"].stats(exchange["pair"]))
            exchange["price"] = exchange["client"].ticker(exchange["pair"])[2]

        elif exchange == exchanges[BTCMARKETS]:

            print("placeholder reached")

    return(exchanges)
