from bs4 import BeautifulSoup
import requests
import os
import csv
import re



# import ticker symbols csv file
filename = 'tsx100.csv'

def parseTickers(file):
    tickers = []
    with open(file, 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in spamreader:
            tickers.append(row[0])
    #ticker is an array that holds all symbols from TSX100
    return tickers


def scrapYahooPage(ticker):
    # craft url query
    stock = ticker
    # month, day, year
    start_month = '03'
    start_day = '1'
    start_year = '1996'
    end_month = '00'
    end_day = '1'
    end_year = '2014'
    pg = 0
    # open CSV writer
    csvfile = open(ticker+'.csv', 'wb')
    writer = csv.writer(csvfile)
    for i in range(67):
        url = 'https://ca.finance.yahoo.com/q/hp?s=' + stock + '.TO&a=' + start_month + '&b='+start_day+'&c='+start_year + '&d=' + end_month + '&e=' + end_day + '&f='+end_year+'&g=d&z=66&y='+str(pg)
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        data = soup.find(attrs={'class': 'yfnc_datamodoutline1'})
        try:
            rows = data.findAll('td')
        except Exception:
            print "Error in finding td tags for: " + ticker
            pass
        datarow = []
        lastdate = " "
        k = 1
        for row in rows:
            box = row.findAll(text=True)
            txt = ','.join(box)
            if "Close" not in txt and "Dividend" not in txt and "-" not in txt and lastdate != txt:  # filters out dividend num, last row
                # this box contains stock info
                datarow.append(txt)
                if re.search('[a-zA-Z]+', txt):
                    lastdate = txt
                if not (k % 7):
                    writer.writerow(datarow)
                    datarow = []

                k += 1

        pg += 66


# loop over each ticker and get data
tickers = parseTickers(filename)

offset = 0
for ticker in tickers:
    # now at CFP, 62
    if offset > 60:
        print ticker + " Stock index: " + str(offset)
        scrapYahooPage(ticker)
    offset += 1


# output to a csv


