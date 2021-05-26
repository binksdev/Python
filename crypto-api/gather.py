import os

import requests
import datetime

import pandas as pd

year  = datetime.datetime.today().year 
month = datetime.datetime.today().month
day   = datetime.datetime.today().day

# convert given date to epoch time in seconds
# datetime.datetime(year, month, day, hour, minutes)
seconds = datetime.datetime(year, month, day, 23, 59).timestamp()

# Finance Yahoo URL period1 = start, period2 = end
currencies = {
    "BTC": f"https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=1410912000&period2={int(seconds)}&interval=1d&events=history&includeAdjustedClose=true",
    "DOG": f"https://query1.finance.yahoo.com/v7/finance/download/DOGE-USD?period1=1410912000&period2={int(seconds)}&interval=1d&events=history&includeAdjustedClose=true",
    "LTC": f"https://query1.finance.yahoo.com/v7/finance/download/LTC-USD?period1=1410912000&period2={int(seconds)}&interval=1d&events=history&includeAdjustedClose=true",
    "ETH": f"https://query1.finance.yahoo.com/v7/finance/download/ETH-USD?period1=1438905600&period2={int(seconds)}&interval=1d&events=history&includeAdjustedClose=true",
    "BCH": f"https://query1.finance.yahoo.com/v7/finance/download/BCH-USD?period1=1500768000&period2={int(seconds)}&interval=1d&events=history&includeAdjustedClose=true",
    "DSH": f"https://query1.finance.yahoo.com/v7/finance/download/DASH-USD?period1=1410912000&period2={int(seconds)}&interval=1d&events=history&includeAdjustedClose=true",
    "ADA": f"https://query1.finance.yahoo.com/v7/finance/download/ADA-USD?period1=1506816000&period2={int(seconds)}&interval=1d&events=history&includeAdjustedClose=true"
}

def retrieve_data(key="BTC", filename="temp.csv"):

    if filename.endswith(".csv"):

        try:
            request = requests.get(currencies[key])

            with open(filename, 'wb') as file:
                file.write(request.content)

            # Read the content of the CSV file into a DataFrame
            content = pd.read_csv(filename, index_col="Date")
            
            # Convert float types into string
            content['Open']  = content['Open'].astype(str)
            content['High']  = content['High'].astype(str)
            content['Low']   = content['Low'].astype(str)
            content['Close'] = content['Close'].astype(str)
            content['Adj Close'] = content['Adj Close'].astype(str)
            content['Volume'] = content['Volume'].astype(str)

            # Delete temporal file
            os.remove(filename)

            return content.to_dict('index'), None
        
        except KeyError as err:
            print(f"Invalid Key Error: the {err} key is not in the available list")
        
        return {}, "Currency not available"
    
    print("Filename Extension Error: filename must be a comma separated values (.csv)")

    return {}, "Filename Extension Error"