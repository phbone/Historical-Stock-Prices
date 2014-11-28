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

def deleteDuplicates(ticker):
    rows = []
    lastmonth = " "
    with open('output/scrape/'+ticker+'.csv', 'rb') as inputfile:
        reader = csv.reader(inputfile)
        for row in reader:
            key = (row[0], row[1][:5])
            month = key[0][:3]
            if month == lastmonth:
                # 2 consequtive months are the same
                removed = rows.pop()
                print "Removed: " + removed
            rows.append(row)
            lastmonth = month

    with open('output/delete/'+ticker+'.csv', 'wb') as outputfile:
        writer = csv.writer(outputfile)
        for row in rows:
            writer.writerow([row[0], row[1]])



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
    print "Processing Stock ("+str(index)+"): " + ticker
    deleteDuplicates(ticker)
    index +=1
# output to a csv


