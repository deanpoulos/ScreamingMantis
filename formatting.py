# messages and escape sequences ==============================================#

GRN = '\033[00;92m'
BLU = '\033[00;94m'
ORG = '\033[00;00;38;5;215m'
RED = '\033[91m'
WHT = '\033[00;01m'
CLR = '\033[00;00m'
YEL = '\033[00;38;5;226m'
LIM = '\033[38;5;190m'
TEL = '\033[38;5;30m'

BINANCE     =   0
KUCOIN      =   1
BTCMARKETS  =   2 % 2
BITFINEX    =   3 % 2

INTRO_MSG   =   ("{0}ScreamingMantis: {1}Prints info about trading " +
                 "pairs through exchange API{2}").format(WHT, YEL, CLR)

EXCHANGES   =    "{0}Loaded Exchanges: ".format(WHT)

NO_DATA     =    "{0}     Couldn't find data here{1}".format(RED, CLR)

ACTIVE      =    GRN + "[TRADING]" + CLR 

INACTIVE    =    RED + "[BREAK]"   + CLR 
