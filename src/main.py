import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import http.client
import json
import datetime


def getData():
    """
    Recopilacion de la informacion:
    1- src/data/sismosMundiales.csv
        data recopilada mediante scraping y formulada en csv
    2- src/data/sismosMundialesModificated.csv
        data ya obtenida y transformada y lista para la ejecucion
    """
    df = pd.read_csv(
        'src/data/sismosMundiales.csv',
        sep=",",
        )
    return df

def modifyData():
    """
    data medoficada para una correcta ejcucion
    """
    dfData = getData()
    dfData['GeneralTime'] = pd.to_datetime(dfData['Timestamp'], unit='s')
    dfData.set_index('Timestamp', inplace = True)
    dfData.drop(['Year', 'Month', 'Day', 'Time'], axis = 'columns', inplace=True)
    dfData.replace(to_replace=[None], value=np.nan, inplace=True)
    return dfData

def countriesHighMagnitude(dfData):
    """
    Los 20 sismos mas grandes dentro de 1970 y 2021
    1- grafico representando la magnitud y las regiones de los hechos
    2- grafico las mismas regiones y la profundidad de cada sismo
    """
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)    
    df = dfData.sort_values("Mag", ascending=True)
    dft = df.tail(20)

    ax.barh(dft["Region"], dft["Mag"], color=['#21FF02','#02FFE8','#023CFF','#FF027D','#3D4E58','#32B65C','#B63240','#7102FF','#2802FF','#FF02F3','#02BEFF','#FF0202','#0284FF','#FF7502','#02FF4F','#FFB602','#02FF94','#FFDD02','#8CFF02','#DDFF02'])
    plt.title("Los 20 sismos mas grandes entre 1970 y 2021", fontsize=16)
    plt.ylabel('Region', fontsize=12)
    plt.xlabel('Magnitud Richter', fontsize=12)

    ax1 = fig.add_subplot(2, 1, 2)
    ax1.barh(dft["Region"], dft["Depth"],color=['#21FF02','#02FFE8','#023CFF','#FF027D','#3D4E58','#32B65C','#B63240','#7102FF','#2802FF','#FF02F3','#02BEFF','#FF0202','#0284FF','#FF7502','#02FF4F','#FFB602','#02FF94','#FFDD02','#8CFF02','#DDFF02'])
    plt.title("Profundidad de los sismos", fontsize=16)
    plt.ylabel('Region', fontsize=12)
    plt.xlabel('Profundidad en kilometros bajo nivel del mar', fontsize=12)

def countriesHighDeph(dfData):
    """
    Los 20 sismos mas profundos dentro de 1970 y 2021
    1- grafico representando la profundidad y las regiones de los hechos
    2- grafico las mismas regiones y su magnitud de cada uno
    """
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)    
    df = dfData.sort_values("Depth", ascending=True)
    dft = df.tail(20)
    ax.barh(dft["Region"], dft["Depth"], color=['#21FF02','#02FFE8','#023CFF','#FF027D','#3D4E58','#32B65C','#B63240','#7102FF','#2802FF','#FF02F3','#02BEFF','#FF0202','#0284FF','#FF7502','#02FF4F','#FFB602','#02FF94','#FFDD02','#8CFF02','#DDFF02'])
    plt.title("Los 20 sismos mas profundos entre 1970 y 2021", fontsize=16)
    plt.ylabel('Region', fontsize=12)
    plt.xlabel('Profundidad en kilometros bajo nivel del mar', fontsize=12)

    ax1 = fig.add_subplot(2, 1, 2)
    ax1.barh(dft["Region"], dft["Mag"],color=['#21FF02','#02FFE8','#023CFF','#FF027D','#3D4E58','#32B65C','#B63240','#7102FF','#2802FF','#FF02F3','#02BEFF','#FF0202','#0284FF','#FF7502','#02FF4F','#FFB602','#02FF94','#FFDD02','#8CFF02','#DDFF02'])
    plt.title("Profundidad de los sismos", fontsize=16)
    plt.ylabel('Region', fontsize=12)
    plt.xlabel('Magnitud Richter', fontsize=12)

def contrastWithChile(dfData):
    """
    validacion de dicha informacion si a meonor profundidad mayor es el sismo 
    transfiriendolo a la realidad chilena.
    presentando sismos mayores a 6 y presentando su informacion  y una media.
    """
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
    plt.ylabel('Profundidad en kilometros bajo nivel del mar', fontsize=12)

def countries90Days(dfData,GeneralTime):
    """
    funcion lambda obteniendo sismos chilenos mayores a 7 y buscando sismos mundiales 120 dias previos al 
    acontecimiento de magnitud mayor o igual a 7.
    retornando un listado de 10 regiones mas comunes en cada evento, filtrado por fechas, magnitud superior
    a 6 y profundidad menor o igual a 150(maximo de la media representado en el grafico anterior).
    """
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
    df = df[df['Mag']>= 6]
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
    """
    funcion que retorna porcentaje de cada region
    """
    return "{:.1f}%".format(pct) 

def countriesPriorToTheEarthquake(dfData):
    """
    Paises que presentaron sismos 120 dias antes del evento en chile
    """   
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

if __name__ == "__main__":
    #dfData = modifyData()
    dfData = pd.read_csv(
        'src/data/sismosMundialesModificated.csv',
        sep=",",
        )
    
    countriesHighMagnitude(dfData)
    #countriesHighDeph(dfData)
    #contrastWithChile(dfData)
    #countriesPriorToTheEarthquake(dfData)

    plt.show()