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
    start_year = '1960'
    end_month = '10'
    end_day = '10'
    end_year = '2014'
    interval = 'm'
    pg = 0
    lastdate = False
    # open CSV writer
    csvfile = open('output/scrape/'+ticker+'.csv', 'wb')
    writer = csv.writer(csvfile)
    data_available = True
    while data_available:
        url = 'https://ca.finance.yahoo.com/q/hp?s=' + stock + '&a=' + start_month + '&b='+start_day+'&c='+start_year + '&d=' + end_month + '&e=' + end_day + '&f='+end_year+'&g='+interval+'&z=66&y='+str(pg)
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        data = soup.find(attrs={'class': 'yfnc_datamodoutline1'})
        if data:
            try:
                rows = data.findAll('td')
            except Exception:
                if(lastdate):
                    print "Last row of prices: " + str(lastdate)
                else:
                    print "No data available"
                data_available = False
                pass
            daterow = []
            pricerow = []
            lastdate = " "
            lastrow = " "
            month_dict = {'01': 'Jan',
                          '02': 'Feb',
                          '03': 'Mar',
                          '04': 'Apr',
                          '05': 'May',
                          '06': 'Jun',
                          '07': 'Jul',
                          '08': 'Aug',
                          '09': 'Sep',
                          '10': 'Oct',
                          '11': 'Nov',
                          '12': 'Dec'}
            # filter out rows for page end, dividend, split
            exclude = ['Close', 'Dividend', ":", "Split"]
            k = 1
            for row in rows:
                box = row.findAll(text=True)
                txt = ','.join(box)
                if not any(sub in txt for sub in exclude) and lastdate != txt:  # filters out dividend num, last row
                    # this box contains stock info
                    if re.search('[a-zA-Z]+', txt):
                        lastdate = txt
                        if re.search('[a-zA-Z]+', lastrow):
                            # dividends being paid
                            daterow = []
                            k +=6
                        daterow.append(txt)
                    elif '-' in txt:
                        # dates formatted differently
                        datetxt = txt.replace("-", " ")
                        day = str(datetxt[8:11])
                        mon = str(datetxt[5:7])
                        year = str(datetxt[:4])
                        newdate = str(month_dict.get(mon)) + " " + day + " " + year
                        lastdate = newdate
                        if re.search('[a-zA-Z]+', lastrow):
                            # dividends being paid
                            daterow = []
                            k +=6
                        daterow.append(newdate)
                    else:
                        pricerow.append(txt)
                    if not (k % 7):
                        # change to datarow for entire row on Yahoo
                        pricedate = daterow[0].replace(",", "")
                        writer.writerow([pricedate, pricerow[0]])
                        daterow = []
                        pricerow = []
                    k += 1
                    lastrow = txt
            pg += 66
            if pg > 594:
                data_available = False
        else:
            if(lastdate):
                print "Last row of prices: " + str(lastdate)
            else:
                print "No data available on: " + ticker
            data_available = False



# import ticker symbols csv file
filename = 'input/oldsp500.csv'
offset = int(raw_input("Enter an offset to start: "))
index = 0

# loop over each ticker and get data
tickers = parseTickers(filename)
print "Fetching from file: " + filename + "..."


for ticker in tickers:

    # for .csv in ticker symbol
    ticker = ticker.replace('.csv', '')
    # for wikipedia stock names
    ticker = ticker.replace('.', '-')

    # now at EQR, 170
    if index >= offset:
        print "Scraping Stock ("+str(index)+"): " + ticker
        scrapYahooPage(ticker)
    index += 1


# output to a csv


