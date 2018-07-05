# Agenda: =====================================================================#
# x add difference between closing prices on primitive example
# x add two more exchanges: Bitfinex & BTC Markets                             
# / add buy/sell order price comparison                                       
# x implement dynamic exchange information fetching for BTCMarkets & Bitfinex
# x implement price comparisons between BTCMarkets & Bitfinex

# library headers ============================================================#

import keys             # abstract away our keys so we improve security
import requests         # so we can contact BTCMarkets API directly
import datetime;        import time                 # for system clock time
from formatting         import *                    # abstract away esc seqs
from binance.client     import Client     as bin    # from python-binance pip
from kucoin.client      import Client     as kuc    # from python-kucoin pip
from btcmarkets.api     import BTCMarkets as btc    # from BTCMarkets github
from bitfinex.client    import Client     as bit    # from bitfinex pip

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
        print("{0} • Closing Prices: {1}".format(WHT, CLR))
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
        initialises the dynamic data for exchanges BTCMarkets and Bitfinex 
        such as price action and trading status
    """

    for exchange in exchanges:

        if exchange == exchanges[BITFINEX]:
            # get medium for bid price
            exchange["price"] = \
            exchange["client"].ticker(exchange["pair"])
            # get status
            exchange["status"] = int(exchange["price"] == {})     * INACTIVE + \
                                 int(not exchange["price"] == {}) * ACTIVE 

        elif exchange == exchanges[BTCMARKETS]:
            # get medium for ask price
            url = exchange["client"].base_url + "/market/" + \
                  exchange["pair"] + "/tick"

            exchange["price"] = requests.get(url, verify=True).json()

            # get status
            exchange["status"] = int(exchange["price"] == {})     * INACTIVE + \
                                 int(not exchange["price"] == {}) * ACTIVE 
            
    return(exchanges)



def printTickInfoBTCMarketsBitfinex(exchanges):
    """
        print most recent price information for BTCMarkets & Bitfinex
    """

    for exchange in exchanges:
        # print name, exchange and status
        print("{0}Trading Pair: {1} {2}{3} {4}".format(WHT, exchange["name"], 
            CLR, exchange["pair"], exchange["status"]))

        # convert timestamp to readable string
        exchange["price"]["timestamp"] = datetime.datetime.fromtimestamp(
                exchange["price"]["timestamp"]).strftime("%H:%M:%S")

        # print bid price compared with asking price
        if exchange == exchanges[BITFINEX]:
            print("{0} • Bid Price:  {1}".format(WHT, CLR), end = '')
            print("{0}{1:.6f} {2}{3}".format(
                                             CLR, exchange["price"]["bid"],
                                             RED, exchange["price"]["timestamp"]))
            print("{0} • Last Price: {1}".format(WHT, CLR), end = '')
            print("{0}{1:.6f} {2}{3}".format(
                                             CLR, exchange["price"]["last_price"],
                                             RED, exchange["price"]["timestamp"]))
            
        if exchange == exchanges[BTCMARKETS]:
            print("{0} • Ask Price:  {1}".format(WHT, CLR), end = '')
            print("{0}{1:.6f} {2}{3}".format(
                                             CLR, exchange["price"]["bestAsk"],
                                             RED, exchange["price"]["timestamp"]))
            print("{0} • Last Price: {1}".format(WHT, CLR), end = '')
            print("{0}{1:.6f} {2}{3}".format(
                                             CLR, exchange["price"]["lastPrice"],
                                             RED, exchange["price"]["timestamp"]))



def profitabilityBTCMarketsBitfinex(exchanges):
    """
        uses a formula to determine the profitability of a trade
    """

    # relative file name
    filename = 'logs/' + time.strftime("%Y-%m-%d")
    print("{0}Printing data to {1}{2}{3}:".format(WHT, YEL + UND, filename, CLR))

    # loop until we terminate the program to keep data up to date
    while 1:

        # calculate percentage 'p' with fees
        import random               # remove once replaced with proper math
        p = random.random()*14 + 94 # placeholder for lyndon's magic

        # open file 'f' for appending lines
        with open(filename, 'a+') as f:

            # initialise line as 'Sat Jul 7 10:00:00 2000  102.53%'
            l = time.strftime("%c", time.localtime()) 
            l += GRN * int(p > 100) + RED * int(p < 100) 
            l += " {0:.2f}%\n".format(p) + CLR

            # print to screen & write to file
            print(CLR + " • " + l, end = '');   f.write(l)

        # wait until data has changed
        time.sleep(3)
        
# BTCMarkets & Binance ========================================================#

def initialiseBTCMarketsBinance(exchanges):
    """
        initialises the dynamic data for exchanges Binance and BTCMarkets such as
        price action and trading status
    """

    # find status (active or inactive) and price data for two exchanges
    for exchange in exchanges:
        # account for some differences in API client
        if exchange == exchanges[BINANCE]:
            # get price history
            exchange["price"] = exchange["client"].get_order_book(symbol=exchange["pair"])            
            # create pseudo timestamp
            exchange["price"]["timestamp"] = int(time.time())

            # get status info
            exchange["status"] = \
            exchange["client"].get_symbol_info(exchange["pair"])["status"]
            exchange["status"] = \
            (int(not (exchange["status"].find("TRADING") == -1)) * ACTIVE) \
               + (int(exchange["status"].find("TRADING") == -1)  * INACTIVE)

        elif exchange == exchanges[BTCMARKETS]:
            # get medium for ask price
            url = exchange["client"].base_url + "/market/" + \
                  exchange["pair"] + "/orderbook"

            exchange["price"] = requests.get(url, verify=True).json()

            # get status
            exchange["status"] = int(exchange["price"] == {})     * INACTIVE + \
                                 int(not exchange["price"] == {}) * ACTIVE 

    return exchanges



def printTickInfoBTCMarketsBinance(exchanges):
    """
        print most recent price information for BTCMarkets & Binance
    """

    for exchange in exchanges:
        # print name, exchange and status
        print("{0}Trading Pair: {1} {2}{3} {4}".format(WHT, exchange["name"], 
            CLR, exchange["pair"], exchange["status"]))

        # convert timestamp to readable string
        exchange["price"]["timestamp"] = datetime.datetime.fromtimestamp(
                exchange["price"]["timestamp"]).strftime("%H:%M:%S")

        # print bid price compared with asking price
        if exchange == exchanges[BINANCE]:
            print("{0} • Bid Price:  {1}".format(WHT, CLR), end = '')
            print("{0}{1} {2}{3}".format(
                                             CLR, exchange["price"]["bids"][0][0],
                                             RED, exchange["price"]["timestamp"]))
            
        if exchange == exchanges[BTCMARKETS]:
            print("{0} • Ask Price:  {1}".format(WHT, CLR), end = '')
            print("{0}{1:.6f} {2}{3}".format(
                                             CLR,
                                             exchange["price"]["asks"][0][0],
                                             RED, exchange["price"]["timestamp"]))



def profitabilityBTCMarketsBinance(exchanges):
    """
        uses a formula to determine the profitability of a trade
    """

    # some constants for price comparison
    initial = float(input("Enter initial amount: "))

    BTCmarketsTradingFee = 0.9915
    BinanceTradingFee = 0.999
    XRPTransferFee = 0.15
    ETHTransferFee = 0.01

    # relative file name
    filename = 'logs/' + time.strftime("%Y-%m-%d")
    print("{0}Printing data to {1}{2}{3}:".format(WHT, YEL + UND, filename, CLR))

    # loop until we terminate the program to keep data up to date
    while 1:

        # reinitialise info to keep it current
        exchanges = initialiseBTCMarketsBinance(exchanges)
        XRPprice = float(exchanges[BTCMARKETS]["price"]["asks"][0][0])
        XRPETHprice = float(exchanges[BINANCE]["price"]["bids"][0][0]) 
        ETHprice = float(requests.get("https://api.btcmarkets.net/market/ETH/AUD/orderbook", 
                                      verify=True).json()["bids"][0][0])

        # calculate percentage 'p' with fees
        AmountXRP = ((initial*BTCmarketsTradingFee)/XRPprice)-XRPTransferFee
        EthAmount = (AmountXRP*XRPETHprice*BinanceTradingFee)-ETHTransferFee
        final = EthAmount*ETHprice*BTCmarketsTradingFee

        p = (final/initial)*100

        # open file 'f' for appending lines
        with open(filename, 'a+') as f:

            # initialise line as 'Sat Jul 7 10:00:00 2000  102.53%'
            l = time.strftime("%c", time.localtime()) 
            l += GRN * int(p > 100) + RED * int(p < 100) 
            l += " {0:.2f}%\n".format(p) + CLR

            # print to screen & write to file
            print(CLR + " • " + l, end = '');   f.write(l)

        # wait until data has changed
        time.sleep(30)
 
