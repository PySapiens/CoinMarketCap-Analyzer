from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin
import csv



def cmc_crawler():
    my_url = "https://coinmarketcap.com/historical/20130428/"
    uClient = uReq(my_url) #downloads the website
    page_html = uClient.read() #html of the website
    uClient.close() #closing client

    page_soup = soup(page_html, "html.parser") #html parser

    exchanges_data = {}
    counter = 0

    #get exchanges and links

    table = page_soup.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        number = cols[0].text
        name = cols[1].text
        symbol = cols[2].text
        mcap = cols[3].text
        price = cols[4].text
        circ_sup = cols[5].text
        
        
        
        
     
    
    
        
  #while my_url nicht empty     
  my_url = page_soup.findAll("li", text=Next Week)
    
    uClient = uReq(my_url) #downloads the website
    page_html = uClient.read() #html of the website
    uClient.close() #closing client
    
    
    
    
    
    
    
    
    for header in page_soup.select(".volume-header"):
        counter = counter + 1
        if counter <= 3: #limitiert auf nummer an exchanges!!!
            exchange_name = header.select_one("a").text
            exchange_url = urljoin(my_url,header.select_one("a").attrs["href"])
        else:
            break
        print(exchange_name)
        print(exchange_url)

        #go to exchange url
        uClient_exchange = uReq(exchange_url)
        page_html_exchange = uClient_exchange.read()
        uClient_exchange.close()

        page_soup_exchange = soup(page_html_exchange, "html.parser")

        pairs_volumes = []
        table = page_soup_exchange.find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            pair = cols[2].text.split("/") #cols[2].text
            volume = row.select_one(".volume").attrs["data-usd"]

            pairs_volumes.append([pair, volume])

        exchanges_data[exchange_name] = pairs_volumes

    print(exchanges_data)
    
    return exchanges_data

def csv_writer(dict):
    with open('cmc_exchanges.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key, value in dict.items():
            writer.writerow([key, value])


#csv_writer(cmc_crawler())
