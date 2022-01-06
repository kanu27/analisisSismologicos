import pandas as pd
import numpy as np
import matplotlib
import os
import http.client
import json


def getData():
    df = pd.read_csv(
        'src/data/sismosMundiales.csv',
        sep=",",
        )
    return df.head()

def getCountry(df):
    lati = df['Lat'].values[0]
    long = df['Lon'].values[0]
    data = {"plus_code":{"compound_code":"33HQ+6H5 Kalkan/Simav/Kütahya, Turkey","global_code":"8GFF33HQ+6H5"},"results":[{"address_components":[{"long_name":"33HQ+6H","short_name":"33HQ+6H","types":["plus_code"]},{"long_name":"Kalkan","short_name":"Kalkan","types":["administrative_area_level_3","political"]},{"long_name":"Simav","short_name":"Simav","types":["administrative_area_level_2","political"]},{"long_name":"Kütahya","short_name":"Kütahya","types":["administrative_area_level_1","political"]},{"long_name":"Turkey","short_name":"TR","types":["country","political"]}],"formatted_address":"33HQ+6H Kalkan/Simav/Kütahya, Turkey","geometry":{"bounds":{"northeast":{"lat":39.078125,"lng":29.089},"southwest":{"lat":39.078,"lng":29.088875}},"location":{"lat":39.078,"lng":29.089},"location_type":"GEOMETRIC_CENTER","viewport":{"northeast":{"lat":39.0794114802915,"lng":29.0902864802915},"southwest":{"lat":39.0767135197085,"lng":29.0875885197085}}},"place_id":"GhIJQ4ts5_uJQ0AREFg5tMgWPUA","plus_code":{"compound_code":"33HQ+6H Kalkan/Simav/Kütahya, Turkey","global_code":"8GFF33HQ+6H"},"types":["plus_code"]},{"address_components":[{"long_name":"İsimsiz Yol","short_name":"İsimsiz Yol","types":["route"]},{"long_name":"Kalkan","short_name":"Kalkan","types":["administrative_area_level_3","political"]},{"long_name":"Simav","short_name":"Simav","types":["administrative_area_level_2","political"]},{"long_name":"Kütahya","short_name":"Kütahya","types":["administrative_area_level_1","political"]},{"long_name":"Turkey","short_name":"TR","types":["country","political"]},{"long_name":"43500","short_name":"43500","types":["postal_code"]}],"formatted_address":"İsimsiz Yol, 43500 Kalkan/Simav/Kütahya, Turkey","geometry":{"bounds":{"northeast":{"lat":39.0785715,"lng":29.0901056},"southwest":{"lat":39.07595999999999,"lng":29.0871719}},"location":{"lat":39.0774744,"lng":29.0882947},"location_type":"GEOMETRIC_CENTER","viewport":{"northeast":{"lat":39.07861473029149,"lng":29.0901056},"southwest":{"lat":39.0759167697085,"lng":29.0871719}}},"place_id":"ChIJ0wOakFdAyBQRmNQzwdpW29o","types":["route"]},{"address_components":[{"long_name":"43502","short_name":"43502","types":["postal_code"]},{"long_name":"Kütahya","short_name":"Kütahya","types":["administrative_area_level_1","political"]},{"long_name":"Turkey","short_name":"TR","types":["country","political"]}],"formatted_address":"43502 Kütahya, Turkey","geometry":{"bounds":{"northeast":{"lat":39.099838,"lng":29.106151},"southwest":{"lat":39.0277,"lng":29.0493709}},"location":{"lat":39.0735397,"lng":29.0809012},"location_type":"APPROXIMATE","viewport":{"northeast":{"lat":39.099838,"lng":29.106151},"southwest":{"lat":39.0277,"lng":29.0493709}}},"place_id":"ChIJrU4PizhAyBQRqLraiVPJe34","types":["postal_code"]},{"address_components":[{"long_name":"Kalkan","short_name":"Kalkan","types":["administrative_area_level_3","political"]},{"long_name":"Simav","short_name":"Simav","types":["administrative_area_level_2","political"]},{"long_name":"Kütahya","short_name":"Kütahya","types":["administrative_area_level_1","political"]},{"long_name":"Turkey","short_name":"TR","types":["country","political"]}],"formatted_address":"Kalkan/Simav/Kütahya, Turkey","geometry":{"bounds":{"northeast":{"lat":39.109858,"lng":29.092587},"southwest":{"lat":39.0387111,"lng":29.042451}},"location":{"lat":39.0735082,"lng":29.0634479},"location_type":"APPROXIMATE","viewport":{"northeast":{"lat":39.109858,"lng":29.092587},"southwest":{"lat":39.0387111,"lng":29.042451}}},"place_id":"ChIJG133H2RAyBQRwLHAx1skPCU","types":["administrative_area_level_3","political"]},{"address_components":[{"long_name":"Simav","short_name":"Simav","types":["administrative_area_level_2","political"]},{"long_name":"Kütahya","short_name":"Kütahya","types":["administrative_area_level_1","political"]},{"long_name":"Turkey","short_name":"TR","types":["country","political"]}],"formatted_address":"Simav/Kütahya, Turkey","geometry":{"bounds":{"northeast":{"lat":39.5436679,"lng":29.233993},"southwest":{"lat":38.855302,"lng":28.6131111}},"location":{"lat":39.2069032,"lng":28.9062794},"location_type":"APPROXIMATE","viewport":{"northeast":{"lat":39.5436679,"lng":29.233993},"southwest":{"lat":38.855302,"lng":28.6131111}}},"place_id":"ChIJ9aGBRjM6yBQRDLjIX1kvnbY","types":["administrative_area_level_2","political"]},{"address_components":[{"long_name":"Kütahya","short_name":"Kütahya","types":["administrative_area_level_1","political"]},{"long_name":"Turkey","short_name":"TR","types":["country","political"]}],"formatted_address":"Kütahya, Turkey","geometry":{"bounds":{"northeast":{"lat":39.9070431,"lng":30.4621429},"southwest":{"lat":38.79054,"lng":28.603224}},"location":{"lat":39.358137,"lng":29.6035495},"location_type":"APPROXIMATE","viewport":{"northeast":{"lat":39.9070431,"lng":30.4621429},"southwest":{"lat":38.79054,"lng":28.603224}}},"place_id":"ChIJcd7mch4DyRQR2MtOz3EXbg8","types":["administrative_area_level_1","political"]},{"address_components":[{"long_name":"Turkey","short_name":"TR","types":["country","political"]}],"formatted_address":"Turkey","geometry":{"bounds":{"northeast":{"lat":42.3666999,"lng":44.8178449},"southwest":{"lat":35.8085919,"lng":25.5377}},"location":{"lat":38.963745,"lng":35.243322},"location_type":"APPROXIMATE","viewport":{"northeast":{"lat":42.3666999,"lng":44.8178449},"southwest":{"lat":35.8085919,"lng":25.5377}}},"place_id":"ChIJcSZPllwVsBQRKl9iKtTb2UA","types":["country","political"]}],"status":"OK"}
    """conn = http.client.HTTPSConnection("maps.googleapis.com")
    payload = ''
    headers = {}
    conn.request("GET", "/maps/api/geocode/json?latlng={},{}&key={}".format(lati,long,os.getenv('googleKeys')), payload, headers)
    res = conn.getresponse()
    data = str(res.read().decode("utf-8")).replace("n","")
    data = json.loads(data.replace("  ",""))"""
    df['Country'] = df['Country'].replace(np.nan, data["results"][6]["formatted_address"])
    print(df)    
    return df

def modifyData():
    global dfData
    dfData = getData()
    dfData['GeneralTime'] = pd.to_datetime(dfData['Timestamp'], unit='s')
    dfData.set_index('Timestamp', inplace = True)
    name = dfData["Region"].str.split(',',expand=True)
    name.columns = ['Location', 'Country']
    dfData = pd.concat([dfData, name], axis=1)
    dfData.drop(['Year', 'Month', 'Day', 'Time', 'Region'], axis = 'columns', inplace=True)
    dfData.replace(to_replace=[None], value=np.nan, inplace=True)
    dfData.apply(lambda row: getCountry(dfData[dfData['Country'].isnull()]),axis=1)
    print("__________________________________________________________")
    print(dfData)




    
if __name__ == "__main__":
    modifyData()



