from bs4 import BeautifulSoup
import requests
import os
import csv
import re

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
    start_month = '00'
    start_day = '1'
    start_year = '1980'
    end_month = '06'
    end_day = '1'
    end_year = '2014'
    pg = 0
    # open CSV writer
    csvfile = open(ticker+'.csv', 'wb')
    writer = csv.writer(csvfile)
    data_available = True
    while data_available:
        url = 'https://ca.finance.yahoo.com/q/hp?s=' + stock + '&a=' + start_month + '&b='+start_day+'&c='+start_year + '&d=' + end_month + '&e=' + end_day + '&f='+end_year+'&g=d&z=66&y='+str(pg)
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        data = soup.find(attrs={'class': 'yfnc_datamodoutline1'})
        try:
            rows = data.findAll('td')
        except Exception:
            if(lastdate):
                print "Last row of prices: " + str(lastdate)
            else:
                print "No data available"
            data_available = False
            pass
        datarow = []
        lastdate = " "
        # filter out rows for page end, dividend, split
        exclude = ['Close', 'Dividend', "-", ":"]
        k = 1
        for row in rows:
            box = row.findAll(text=True)
            txt = ','.join(box)
            if not any(sub in txt for sub in exclude) and lastdate != txt:  # filters out dividend num, last row
                # this box contains stock info
                datarow.append(txt)
                if re.search('[a-zA-Z]+', txt):
                    lastdate = txt
                if not (k % 7):
                    writer.writerow(datarow)
                    datarow = []
                k += 1
        pg += 66



# import ticker symbols csv file
filename = 's&p500.csv'
offset = int(raw_input("Enter an offset to start: "))
index = 0

# loop over each ticker and get data
tickers = parseTickers(filename)
print "Fetching from file: " + filename + "..."

for ticker in tickers:
    ticker = ticker.replace('.', '-')
    # now at EQR, 170
    if index >= offset:
        print "Scraping Stock ("+str(index)+"): " + ticker
        scrapYahooPage(ticker)
    index += 1


# output to a csv


