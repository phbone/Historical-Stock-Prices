from bs4 import BeautifulSoup
import requests
import os
import csv
import re
from collections import deque
import csv


def parseTickers(file):
    tickers = []
    with open(file, 'rU') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in spamreader:
            tickers.append(row[0])
    #ticker is an array that holds all symbols from TSX100
    return tickers


def get_last_row(csv_filename):
    with open(csv_filename, 'rb') as f:
        return deque(csv.reader(f), 1)[0]

def getColumns(csv_filename):
    with open(csv_filename, 'rb') as f:
        print csv.reader(f)

###################################################
# import ticker symbols csv file
filename = 's&p500.csv'


csvfile = open('output/final_dates_'+filename, 'wb')
writer = csv.writer(csvfile)
# loop over each ticker and get data
tickers = parseTickers('input/'+filename)


for ticker in tickers:
    ticker = ticker.replace('.', '-')

    ####
    datarow = get_last_row("S&P500/"+ticker+".csv")
    last_row = datarow[0].replace(",", "")
    row = [ticker, str(last_row)]
    writer.writerow(row)
    # gets the last line of each ticker and stores it file


    columnfile = open('output/short/'+ticker+".csv", 'wb')
    writeshort = csv.writer(columnfile)
    with open('S&P500/'+ticker+'.csv', 'rb') as fa:
        reader = csv.reader(fa, delimiter=',')
        for r in reader:
            writeshort.writerow([r[0].replace(",", ""), str(r[1])])
    print "Finished processing: " + ticker