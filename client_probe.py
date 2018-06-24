#=============================================================================#
#    Screaming Mantis: uses binance & kucoin APIs and prints relevant info    #
#=============================================================================#

# library headers ============================================================#
import keys     # abstract away our keys so we don't compromise security
import datetime;    import time             # for system clock time
from binance.client import Client as bCli   # from python-binance via pip
from kucoin.client  import Client as kCli   # from python-kucoin via pip
from time           import sleep            # to loop program and update 1m

# messages and escape sequences ==============================================#

GRN = '\033[00;92m'
BLU = '\033[94;01m'
ORG = '\033[38;5;215;01m'
RED = '\033[91m'
WHT = '\033[00;01m'
CLR = '\033[00;00m'
YEL = '\033[38;5;226m'

INTRO_MSG = ("{0}ScreamingMantis: {1}Prints info about trading " +
             "pairs through exchange API{2}").format(WHT, YEL, CLR)

EXCHANGES =  "{0}Exchanges: ".format(WHT)


# declaration of static exchange data structure =============================#

binance = { 'client':   bCli(keys.APIKey, keys.SecretKey),
            'name':     ORG + "[BINANCE]" + CLR,
            'pair':     "NEOETH"                           }

kucoin  = { 'client':   kCli(keys.APIKey, keys.SecretKey),
            'name':     BLU + "[KUCOIN]" + CLR,
            'pair':     "NEO-ETH"                           }

exchanges = (binance, kucoin)

# introduce program ==========================================================#

print("\n{0}".format(INTRO_MSG))

for exchange in exchanges:
    EXCHANGES += exchange["name"] + " "
print(EXCHANGES + '\n')

minutes=int(input("Duration of historical data (minutes): "))
start_str=str(minutes) + " min ago UTC"

# initialisation of dynamic exchange data ====================================#

for exchange in exchanges:

    exchange["price"] = []

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
        int(time.time()) - minutes*60, int(time.time()))
        # create pseudo symbol info
        exchange["status"] = \
        exchange["client"].get_tick(exchange["pair"])["trading"]
        exchange["status"] = int(exchange["status"])*"TRADING" + \
                                 (not int(exchange["status"]))*"INACTIVE"


# print contextual exchange/pair information =================================#

for exchange in exchanges:
    # print name, exchange and status
    print("{0}Trading Pair: {1} {2}{3} {4}[{5}]".format(WHT, exchange["name"], 
        CLR, exchange["pair"], GRN, exchange["status"]))

    # print closing prices over interval
    print("{0} - Closing Prices: {1}".format(WHT, CLR))

    for list in exchange["historicalKline"]:
        if not (list[4] == None):
            # calculate age of price using timestamps
            age = int(time.time()) - int(list[0])/1000

            # print price and age of price
            print("     {0}{1} {2}{3} seconds ago".format(CLR, list[4], 
                               RED, age))
            exchange["price"].append({ age: list[4] })

# assert we have at least one entry for price action in kucion
if (kucoin["price"] == []):
    print("{0}     Couldn't find price action for kucoin".format(RED))
    exit()

# calculate difference in price as a percentage of buying price
for entryA in kucoin["price"]:

    entryB = {}

    # iterate over binance until we find a match in price age
    for i in range(0,len(binance["price"])):
        # find binance price entry that corresponds with kucoin
        if (list(entryA.keys())[0] == list(binance["price"][i].keys())[0]):
           entryB = binance["price"][i]
           break

    # calculate and print the difference in prices at a particular age
    age = entryA.keys()[0]
    difference = ((entryA[age] - entryB[age]) /\
                   entry[age]) * 100
    print("Difference is {0}% from {1} seconds ago".format(difference, age))
