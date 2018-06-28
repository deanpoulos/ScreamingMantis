#=============================================================================#
#    Screaming Mantis: uses binance & kucoin APIs and prints relevant info    #
#=============================================================================#

# library headers ============================================================#

import keys              # abstract away our keys so we improve security
import datetime;        import time                 # for system clock time
from formatting         import *                    # abstract away esc seqs
from clientProbe        import *                    # abstract main functions
from time               import sleep                # to loop program update 1m

# declaration of static exchange data structure =============================#

binance    =    { 'client':   bin(keys.APIKey, keys.SecretKey),
                    'name':   ORG + "[Binance]" + CLR,
                    'pair':   "NEOETH"                           }
kucoin     =    { 'client':   kuc(keys.APIKey, keys.SecretKey),
                    'name':   BLU + "[KuCoin]" + CLR,
                    'pair':   "NEO-ETH"                          }
btcmarkets =    { 'client':   btc(keys.APIKey, keys.SecretKey),
                    'name':   LIM + "[BTC Markets]" + CLR,
                    'pair':   "ETH/BTC"                          } 
bitfinex   =    { 'client':   bit(),
                    'name':   TEL + "[Bitfinex]" + CLR,
                    'pair':   "ethbtc"                           }

exchanges  =    [binance, kucoin, btcmarkets, bitfinex]

# introduce program ==========================================================#

print("\n{0}".format(INTRO_MSG) + '\n')

print((EXCHANGES + " ".join([exchange["name"] for exchange in exchanges])+'\n'))

print("") # print new line implicitly

choice      = input(("Select exchange combination:\n\n   1) {0} & {1}" + \
                     "\n   2) {2} & {3}\n\n(1/2): ").format(kucoin["name"],
                        binance["name"], btcmarkets["name"], bitfinex["name"]))

print("") # print new line implicitly

# complete arbitrage depending on exchanges ==================================#

if choice == "1":
    # get time frame for closing prices
    minutes     = int(input("Age of price history (min): ")); print("") 
    start_str   = str(minutes) + "min ago UTC"
    # initialise exchange information
    exchanges = [binance, kucoin]
    exchanges = initialiseKuCoinBinance(exchanges, minutes, start_str)
    # print contextual information
    printTickInfoKuCoinBinance(exchanges); print("") 
    # complete print closing difference between kucoin and binance
    closingDifferenceKuCoinBinance(exchanges); print("") 

elif choice == "2":
    # initialise exchange information
    exchanges = [btcmarkets, bitfinex]
    exchanges = initialiseBTCMarketsBitfinex(exchanges)
    # print contextual information
    printTickInfoBTCMarketsBitfinex(exchanges); print("")
    # calculate profitablity and print to file
    profitabilityBTCMarketsBitfinex(exchanges); print("")
else:
    exit()
