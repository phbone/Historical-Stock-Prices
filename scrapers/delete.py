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
    lastmonth = "Oct"
    with open('input/'+ticker+'.csv', 'rb') as inputfile:
        reader = csv.reader(inputfile)
        headers = next(reader)  # collect first row as headers for the output
        for row in reader:
            key = (row[0], row[1][:5])
            month = key[0][:3]
            if month != lastmonth and key[0][:6] != "May 29":
                # 2 consequtive months are not the same
                rows.append(row)
                lastmonth = month

    with open('output/delete/'+ticker+'.csv', 'wb') as outputfile:
        writer = csv.writer(outputfile)
        for row in rows:
            writer.writerow([row[0], row[1]])



# import ticker symbols csv file
filename = 'input/inflation_tickers.csv'
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
# output to a csv


