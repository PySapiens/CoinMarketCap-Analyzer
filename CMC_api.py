import requests
import json

while True:
    #base URLS
    globalURL = "https://api.coinmarketcap.com/v1/global/"
    tickerURL = "https://api.coinmarketcap.com/v1/ticker/"

    #get data from global URL

    request = requests.get(globalURL)
    data = request.json()
    globalMarketCap = data['total_market_cap_usd']

    #menu
    print()
    print('Welcome to the CMC Explorer')
    print('Global Cap $' + str(globalMarketCap))
    print("Enter 'all' or 'name of crypto' to see the name of all cryptocurrencies ")
    print()
    choice = input('Your choice: ')

    if choice == 'all':
        request = requests.get(tickerURL)
        data = request.json()

        for x in data:
            ticker = x['symbol']
            price = x['price_usd']

            print(ticker + ':\t\t$' + price)
        print()

    else:
        tickerURL += '/'+choice+'/'
        request = requests.get(tickerURL)
        data = request.json()

        ticker = data[0]['symbol']
        price = data[0]['price_usd']

        print(ticker + ':\t\t$' + price)
        print()

    choice2 = input("Again? (y/n: ")
    if choice2 == 'y':
        continue
    if choice2 == 'n':
        break
