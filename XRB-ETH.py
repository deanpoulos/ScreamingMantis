# headers
import requests
import time

# globals
coins       = ('NANO','ETH','USD')
# exchange structure: name, host, priceList 
exchanges   = [("Kucoin",   "https://api.kucoin.com/", {}),
               ("Binance",  "https://api.binance.com", {})]
inputMsg    = "Enter your projected starting Capital: "

# input
intial = float(input(inputMsg))

while True:
    # populate this data type with two different exchanges' price list
    priceList = {}

    # for all coins
    for coin in coins:
        for exchange in exchanges:
            url = "https://api.binance.com/market/" + coin + "/AUD/tick"
            r = requests.get(url, verify=True)
            # log current price from json entry "lastPrice"
            priceList["{0}".format(coin)] = float(r.json()["lastPrice"])
            print(exchange + btcmarketsAUD)

#####################################################################################

        print("BITFINEXBTC")
        print(bitfinexBTC)


        #FEES AXRP --> UXRP --> UBTC --> ABTC
        fixedBTCFee = (0.0005 * btcmarketsAUD["BTC"])
        fixedXRPFee = (0.01 * btcmarketsAUD["XRP"])

        feesBTCBuy = (intial * 0.0085)
        feeBTCBFX = (intial - (feesBTCBuy + fixedBTCFee)) * 0.002
        feesBTCSell = (intial - (feesBTCBuy + feeBTCBFX + fixedXRPFee + fixedBTCFee)) * 0.0085

        feesTotal = float(feesBTCBuy + fixedBTCFee + feeBTCBFX + fixedXRPFee + feesBTCSell)
        print("Fees: " + str("{0:.2f}".format(feesTotal)))

        #FINAL WITHOUT FEES
        final = float(intial/ btcmarketsAUD["BTC"]  / bitfinexBTC['XRP'] * btcmarketsAUD["XRP"])
        print("Final: " + str("{0:.2f}".format(final)))

        #FINAL WITH FEES
        finalWithFees = final - feesTotal
        print("Final with Fees: " + str("{0:.2f}".format(finalWithFees)))



        #PERCENTAGE
        percentage = "{0:.2f}".format(finalWithFees / intial * 100)
        print("Percentage: " + str(percentage) + "%")

        f = open('ExchangeLogBTC-XRP.txt', 'a')
        f.write(str(time.strftime("%c", time.localtime())) + " " + "{0:.2f}".format(finalWithFees) + " " 
                + str(percentage) + "%  " + "BTM: " + str(btcmarketsAUD) + "BFX"+ str(bitfinexBTC) + " \n")
        f.close()

        print("\n")
        time.sleep(10)
