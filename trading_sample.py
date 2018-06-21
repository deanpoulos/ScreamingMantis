import keys  # abstract away our keys so we don't compromise security
from binance.client import Client # from python-binance via pip
import datetime # other important libraries
from time import sleep

# initialise our client with our unique keys
client = Client(keys.APIKey, keys.SecretKey)

# trading pair (check accuracy)
symbol = 'XRBETH'

# how much volume (starting volume)
quantity = 0.05

# while we are waiting for the right moment to place an order
order = False
while order==False:
    # using the historical 5m interval data, received as a string
    XRB = client.get_historical_klines(symbol=symbol, interval='5m',
                                       start_str="1 hour ago UTC")
    # using float codes for price types, make a small calculated decision
    # i.e. if 2nd last price is greater than last price by 500 units,
    if (float(XRB[-1][4]) - float(XRB[-2][-4])) > 500:
        # buy the given quantity
        client.order_market_buy(symbol=symbol, quantity=quantity)
        order = True
    elif (float(XRB[-1][4]) - float(XRB[-2][-4])) < -500:
        # sell the given quantity
        client.order_market_sell(symbol=symbol, quantity=quantity)
        order = True
    else:
        # sleep
        sleep(60)
