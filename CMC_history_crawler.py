from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin
import csv


def cmc_history_crawler():
    my_url = "https://coinmarketcap.com/historical/20130428/"
    uClient = uReq(my_url)  # downloads the website
    page_html = uClient.read()  # html of the website
    uClient.close()  # closing client
    page_soup = soup(page_html, "html.parser")  # html parser

    # link to next week
    paginator = page_soup.select(".pagination")[0]
    link_nw = paginator.findAll('a', href=True)[1].attrs["href"]
    # go to next week, --> muss man glaube ich nicht
    #ck_uClient = uReq(link_nw)  # downloads the website
    #ck_page_html = ck_uClient.read()  # html of the website
    #ck_uClient.close()  # closing client
    # html von next week
    #ck_page_soup = soup(ck_page_html, "html.parser")  # html parser
    # link to next next week
    #ck_paginator = ck_page_soup.select(".pagination")[0]
    #ck_link_nw = ck_paginator.findAll('a', href=True)[1].attrs["href"]

    # main loop, history container
    history = []
    counter_date = 0
    #while link to next week is not empty
    while link_nw != '':
        # uClient = uReq(my_url)  # downloads the website
        # page_html = uClient.read()  # html of the website
        # uClient.close()  # closing client
        # page_soup = soup(page_html, "html.parser")  # html parser

        date = page_soup.find_all('h1')[1].text.split("- ")[1].strip
        print(date)
        table = page_soup.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        max_crcs = 100
        counter = 0

        for row in rows:
            cols = row.find_all('td')
            number = cols[0].text.strip
            name = cols[1].text.strip
            symbol = cols[2].text.strip
            mcap = cols[3].text.strip
            price = cols[4].text.strip
            circ_sup = cols[5].text.strip

            history.append([date, number, name, symbol, mcap, price, circ_sup])
            counter += 1

            if counter >= 100: # max 100 cryptocurrencies
                break

        # url auf nächste seite ändern
        if page_soup.select(".pagination")[0] !='': #if there is a paginator
            paginator = page_soup.select(".pagination")[0]#get pagination
            url_date = paginator.findAll('a', href=True)[1].attrs["href"]#get url extension for next week
            my_url = urljoin('https://coinmarketcap.com/historical/', url_date)#merge urls
            uClient = uReq(my_url)  # downloads the website
            page_html = uClient.read()  # html of the website
            uClient.close()  # closing client
            page_soup = soup(page_html, "html.parser")  # html parser
            paginator = page_soup.select(".pagination")[0]
            link_nw = paginator.findAll('a', href=True)[1].attrs["href"]
            counter_date += 1
        else:
            link_nw = ''

        if counter_date == 3:
            link_nw = ''

    return (history)


def csv_writer(history):
    with open('cmc_history.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for date, number, name, symbol, mcap, price, circ_sup in history:
            writer.writerow([date, number, name, symbol, mcap, price, circ_sup])

csv_writer(cmc_history_crawler())
