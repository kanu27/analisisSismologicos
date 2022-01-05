import pandas as pd
import numpy as np
import matplotlib
import os
import http.client



def getData():
    df = pd.read_csv(
        'src/data/sismosMundiales.csv',
        sep=",",
        )
    return df.head()

def GetCountry(df):
    conn = http.client.HTTPSConnection("maps.googleapis.com")
    payload = ''
    headers = {}
    conn.request("GET", "/maps/api/geocode/json?latlng=43.609,12.336&key=AIzaSyCQrCqobvEVkWXFdyUUsKXo4KHg-520Lr8", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    lati = df['Lat']
    long = df['Lon']
    df.replace({"0-17": 17, "+55": 60})

def modifyData():
    dfDate = getData()
    dfDate['GeneralTime'] = pd.to_datetime(dfDate['Timestamp'], unit='s')
    dfDate.set_index('Timestamp', inplace = True)
    name = dfDate["Region"].str.split(',',expand=True)
    name.columns = ['Location', 'Country']
    dfDate = pd.concat([dfDate, name], axis=1)
    dfDate.drop(['Year', 'Month', 'Day', 'Time', 'Region'], axis = 'columns', inplace=True)
    dfDate.replace(to_replace=[None], value=np.nan, inplace=True)
    
    #print()
    autopct=lambda country: GetCountry(dfDate[dfDate['Country'].isnull()])
 















    
if __name__ == "__main__":
    modifyData()



