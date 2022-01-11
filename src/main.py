import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import http.client
import json

#Year,Month,Day,Time,Lat,Lon,Depth,Mag,Region,Timestamp
#2011,06,14,23:57:56,29.33,130.99,16,3,"RYUKYU ISLANDS, JAPAN",1308095876

def getData():    
    df = pd.read_csv(
        'src/data/sismosMundiales.csv',
        sep=",",
        )
    return df

def getCountry(lat,lon,ct):
    respon = "City"
    try:
        if type(ct) == float:
            lati = lat
            long = lon            
            conn = http.client.HTTPSConnection("maps.googleapis.com")
            payload = ''
            headers = {}
            conn.request("GET", "/maps/api/geocode/json?latlng={},{}&key={}".format(lati,long,os.getenv('googleKeys')), payload, headers)
            res = conn.getresponse()
            data = str(res.read().decode("utf-8")).replace("n","")
            data = json.loads(data.replace("  ",""))
            respon = str(data["results"][-1]["formatted_address"]).upper()
        else:
            respon = ct
    except OSError as error:
        print(lati,long)
        print(error)
    except Exception as error:
        print(lati,long)
        print(error)
    return respon

def modifyData():
    dfData = getData()
    dfData['GeneralTime'] = pd.to_datetime(dfData['Timestamp'], unit='s')
    dfData.set_index('Timestamp', inplace = True)
    #name = dfData["Region"].str.split(',',expand=True)
    #name.columns = ['Location', 'Country']
    #dfData = pd.concat([dfData, name], axis=1)
    dfData.drop(['Year', 'Month', 'Day', 'Time'], axis = 'columns', inplace=True)
    dfData.replace(to_replace=[None], value=np.nan, inplace=True)
    #dfData["Country"] = dfData.apply(lambda row: getCountry(row["Lat"],row["Lon"],row["Country"]),axis=1)    
    dfData.to_csv("src/data/sismosMundialesModificated.csv")
    return dfData

def countriesHighMagnitude(dfData):
    """Paises con sismos de magnitud mayor  o igual a 8"""
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)    
    df = dfData.sort_values("Mag", ascending=True)
    dft = df.tail(20)

    ax.barh(dft["Region"], dft["Mag"], color=['#21FF02','#02FFE8','#023CFF','#FF027D','#3D4E58','#32B65C','#B63240','#7102FF','#2802FF','#FF02F3','#02BEFF','#FF0202','#0284FF','#FF7502','#02FF4F','#FFB602','#02FF94','#FFDD02','#8CFF02','#DDFF02'])
    plt.title("Los 20 sismos mas grandes entre 1970 y 2021", fontsize=16)
    plt.ylabel('Pais', fontsize=12)
    plt.xlabel('Magnitud Richter', fontsize=12)

    ax1 = fig.add_subplot(2, 1, 2)
    ax1.barh(dft["Region"], dft["Depth"],color=['#21FF02','#02FFE8','#023CFF','#FF027D','#3D4E58','#32B65C','#B63240','#7102FF','#2802FF','#FF02F3','#02BEFF','#FF0202','#0284FF','#FF7502','#02FF4F','#FFB602','#02FF94','#FFDD02','#8CFF02','#DDFF02'])
    plt.title("Profundidad de los sismos", fontsize=16)
    plt.ylabel('Pais', fontsize=12)
    plt.xlabel('Profundidad a nivel del mar en kilometros', fontsize=12)

def countriesHighDeph(dfData):
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)    
    df = dfData.sort_values("Depth", ascending=True)
    dft = df.tail(20)
    ax.barh(dft["Region"], dft["Depth"], color=['#21FF02','#02FFE8','#023CFF','#FF027D','#3D4E58','#32B65C','#B63240','#7102FF','#2802FF','#FF02F3','#02BEFF','#FF0202','#0284FF','#FF7502','#02FF4F','#FFB602','#02FF94','#FFDD02','#8CFF02','#DDFF02'])
    plt.title("Los 20 sismos mas profundos entre 1970 y 2021", fontsize=16)
    plt.ylabel('Pais', fontsize=12)
    plt.xlabel('Profundidad a nivel del mar en kilometros', fontsize=12)

    ax1 = fig.add_subplot(2, 1, 2)
    ax1.barh(dft["Region"], dft["Mag"],color=['#21FF02','#02FFE8','#023CFF','#FF027D','#3D4E58','#32B65C','#B63240','#7102FF','#2802FF','#FF02F3','#02BEFF','#FF0202','#0284FF','#FF7502','#02FF4F','#FFB602','#02FF94','#FFDD02','#8CFF02','#DDFF02'])
    plt.title("Profundidad de los sismos", fontsize=16)
    plt.ylabel('Pais', fontsize=12)
    plt.xlabel('Magnitud Richter', fontsize=12)

def contrastWithChile(dfData):
    #fig = plt.figure()
    #ax = fig.add_subplot(1, 1, 1)
    datasChile = dfData[dfData["Region"].str.contains("CHILE")]
    datasChileHigh6 = datasChile[datasChile["Mag"] >= 6.0]
    dft = datasChileHigh6.sort_values("Mag", ascending=True)
    mean = dft.groupby("Mag").agg("mean")
    #ax.barh(dft["Mag"],dft["Depth"])
    #plt.title("sismos en chile mayores a 6 vs su profundidad", fontsize=16)
    #plt.ylabel('Magnitud Richter', fontsize=12)
    #plt.xlabel('Profundidad a nivel del mar en kilometros', fontsize=12)
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 1, 1)
    ax1.scatter(dft["Mag"],dft["Depth"], marker="o")
    ax1.plot(mean["Depth"])
    plt.title("sismos en chile mayores a 6 vs su profundidad y su media ponderada", fontsize=16)
    plt.xlabel('Magnitud Richter', fontsize=12)
    plt.ylabel('Profundidad a nivel del mar en kilometros', fontsize=12)


def countriesPriorToTheEarthquake(dfData):
    """Paises que presentaron sismos 90 dias antes del evento en chile"""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    datasChile = dfData[dfData["Region"].str.contains("CHILE")]
    datasChileHigh6 = datasChile[datasChile["Mag"] >= 6.0]
    print(datasChileHigh6.head())
    #dataCountry

#https://www.uv.es/vcoll/Curso_de_Introducci%C3%B3n_a_R_files/figure-html/unnamed-chunk-269-1.png
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html

if __name__ == "__main__":
    dfData = pd.read_csv(
        'src/data/sismosMundialesModificated.csv',
        sep=",",
        )
    #countriesHighMagnitude(dfData)
    #countriesHighDeph(dfData)
    contrastWithChile(dfData)
    
    #countriesPriorToTheEarthquake(dfData)

    plt.show()