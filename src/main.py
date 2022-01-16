import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import http.client
import json
import datetime

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
    #dfData.to_csv("src/data/sismosMundialesModificated.csv")
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
    datasChile = dfData[dfData["Region"].str.contains("CHILE")]
    datasChileHigh6 = datasChile[datasChile["Mag"] >= 6.0]
    dft = datasChileHigh6.sort_values("Mag", ascending=True)
    mean = dft.groupby("Mag").agg("mean")
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 1, 1)
    ax1.scatter(dft["Mag"],dft["Depth"], marker="o")
    ax1.plot(mean["Depth"])
    plt.title("sismos en chile mayores a 6 vs su profundidad y su media", fontsize=16)
    plt.xlabel('Magnitud Richter', fontsize=12)
    plt.ylabel('Profundidad a nivel del mar en kilometros', fontsize=12)

def countries90Days(dfData,GeneralTime):
    GeneralTime = datetime.datetime.strptime(GeneralTime, "%Y-%m-%d %H:%M:%S")

    days90Before = GeneralTime - datetime.timedelta(days=120)
    days90BeforeStr = str()
    days90BeforeStr = str(days90Before.year)+"-"    
    if days90Before.month < 10:
        days90BeforeStr += "0"+str(days90Before.month)+"-"
    else:
        days90BeforeStr += str(days90Before.month)+"-"       
    if days90Before.day < 10:
        days90BeforeStr += "0"+str(days90Before.day)+" "
    else:
        days90BeforeStr += str(days90Before.day)+" "
    if days90Before.hour < 10:
        days90BeforeStr += "0"+str(days90Before.hour)+":"
    else:
        days90BeforeStr += str(days90Before.hour)+":"    
    if days90Before.minute < 10:
        days90BeforeStr += "0"+str(days90Before.minute)+":"
    else:
        days90BeforeStr += str(days90Before.minute)+":"    
    if days90Before.second < 10:
        days90BeforeStr += "0"+str(days90Before.second)
    else:
        days90BeforeStr += str(days90Before.second)
    

    GeneralTimeStr = str(GeneralTime.year)+"-"    
    if GeneralTime.month < 10:
        GeneralTimeStr += "0"+str(GeneralTime.month)+"-"
    else:
        GeneralTimeStr += str(GeneralTime.month)+"-"       
    if GeneralTime.day < 10:
        GeneralTimeStr += "0"+str(GeneralTime.day)+" "
    else:
        GeneralTimeStr += str(GeneralTime.day)+" "

    if GeneralTime.hour < 10:
        GeneralTimeStr += "0"+str(GeneralTime.hour)+":"
    else:
        GeneralTimeStr += str(GeneralTime.hour)+":"
    if GeneralTime.minute < 10:
        GeneralTimeStr += "0"+str(GeneralTime.minute)+":"
    else:
        GeneralTimeStr += str(GeneralTime.minute)+":"
    if GeneralTime.second < 10:
        GeneralTimeStr += "0"+str(GeneralTime.second)
    else:
        GeneralTimeStr += str(GeneralTime.second)
    df = dfData.loc[(dfData['GeneralTime'] >= days90BeforeStr) & (dfData['GeneralTime'] < GeneralTimeStr)]
    df = df[df['Depth']<= 150]
    df = df[df['Mag']>= 5]
    df1 = df
    df1["Count"] = 1
    df1["region"] = df["Region"]    
    df1 = df1.groupby("region").agg("sum")
    df1 = df1.sort_values("Count", ascending=True)
    df1 = df1.tail(10)
    df1["Region"] = df1.index
    df1.drop(['Timestamp', 'Lat', 'Lon','Depth','Mag'],axis = 'columns', inplace=True)
    regionList = list()
    for data in df1['Region']:
        regionList.append(data)
    return regionList

def porcentajeValor(pct):
    return "{:.1f}%".format(pct) 

def countriesPriorToTheEarthquake(dfData):
    """Paises que presentaron sismos 120 dias antes del evento en chile"""
   
    datasChile = dfData[dfData["Region"].str.contains("CHILE")]
    datasChileHigh7 = datasChile[datasChile["Mag"] >= 7.0]
    dft = datasChileHigh7.sort_values("Mag", ascending=True)
    regionSeries = dft.apply(lambda row: countries90Days(dfData,row["GeneralTime"]),axis=1) 
    regionList = list()
    for regions in regionSeries:
        for region in regions:
            regionList.append(region)
    df = pd.DataFrame(regionList,columns=['Region'])
    df["Count"] = 1
    df = df.groupby("Region").agg("sum")
    df = df.sort_values("Count", ascending=True)
    df["Region"] = df.index
    df = df.tail(10)

    fig3, ax3 = plt.subplots()
    wedges, texts, autotexts = ax3.pie(df["Count"],
                                      autopct=lambda pct: porcentajeValor(pct),
                                      labels=df["Region"],
                                      shadow=True,
                                      startangle=90,
                                      textprops=dict(color="white"))
    ax3.legend(wedges, df["Region"],
              title="Regiones",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=8, weight="bold")
    ax3.set_title("Regiones sismicas antes de un terremoto en chile")




#https://www.uv.es/vcoll/Curso_de_Introducci%C3%B3n_a_R_files/figure-html/unnamed-chunk-269-1.png
#https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.text.html

if __name__ == "__main__":
    dfData = pd.read_csv(
        'src/data/sismosMundialesModificated.csv',
        sep=",",
        )
    countriesHighMagnitude(dfData)
    countriesHighDeph(dfData)
    contrastWithChile(dfData)
    countriesPriorToTheEarthquake(dfData)

    plt.show()