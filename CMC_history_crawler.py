from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin
import csv



def cmc_crawler():
    my_url = "https://coinmarketcap.com/historical/20130428/"
    uClient = uReq(my_url)  # downloads the website
    page_html = uClient.read()  # html of the website
    uClient.close()  # closing client
    page_soup = soup(page_html, "html.parser")  # html parser

    exchanges_data = {}
    counter = 0

    #link to next week
    paginator = page_soup.select(".pagination")[0]
    link_nw = paginator.findAll('a', href=True)[1].attrs["href"]

    #go to next week
    ck_uClient = uReq(link_nw)  # downloads the website
    ck_page_html = ck_uClient.read()  # html of the website
    ck_uClient.close()  # closing client

    ck_page_soup = soup(ck_page_html, "html.parser")  # html parser

    #link to next next week
    ck_paginator = ck_page_soup.select(".pagination")[0]
    ck_link_nw = ck_paginator.findAll('a', href=True)[1].attrs["href"]

    #if there us a next next week, prepare for loop
    if ck_link_nw == '':
        break
    else:
        uClient = uReq(my_url)  # downloads the website
        page_html = uClient.read()  # html of the website
        uClient.close()  # closing client
        page_soup = soup(page_html, "html.parser")  # html parser


        date = page_soup.find_all('h1')[1].text.split("- ")[1]
        table = page_soup.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        max_crcs = 100
        counter = 0
        for row in rows:
            cols = row.find_all('td')
            number = cols[0].text
            name = cols[1].text
            symbol = cols[2].text
            mcap = cols[3].text
            price = cols[4].text
            circ_sup = cols[5].text

    #url auf nächste seite ändern
    paginator = page_soup.select(".pagination")[0]
    my_url = paginator.findAll('a', href=True)[1].attrs["href"]



def csv_writer(dict):
    with open('cmc_exchanges.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key, value in dict.items():
            writer.writerow([key, value])

#csv_writer(cmc_crawler())
