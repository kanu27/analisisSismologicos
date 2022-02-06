import csv
import os
from calendar import monthrange
from dateutil import rrule, relativedelta
from time import sleep
import datetime
from selenium import webdriver
from helper.database.postgres import PostgresClass

if __name__ == "__main__":
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "/home/kanu/Documentos/Dev/Estudio/analisisSismologicos/src/data/csv"}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "/home/kanu/Documentos/Dev/Estudio/analisisSismologicos/config/chromedriver"
    driver = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
    
    datetimeInit = datetime.datetime.strptime('1970/01/01', '%Y/%m/%d')
    monthss = rrule.rrule(rrule.MONTHLY, dtstart=datetimeInit, until=datetime.datetime.now()).count()
    annoInit = 1970
    monthInit = 0
    annoEnd = 1970
    monthEnd = 0
    countMonth = 1
    for month in range(monthss):
        monthInit += countMonth
        if monthInit > 12:
            monthInit = 1
            annoInit += 1
        val = str(annoInit)
        if monthInit < 10:
            val += "-0"+str(monthInit)
        else:
            val += "-"+str(monthInit)
        val += "-01"

        monthEnd += countMonth
        if monthEnd < 13:
            val1 = str(annoEnd)
            if monthEnd < 10:
                val1 += "-0"+str(monthEnd)
            else:
                val1 += "-"+str(monthEnd)
            val1 += "-"+str(monthrange(annoInit,monthInit)[1])
            try:
                driver.get("http://www.iris.washington.edu/ieb/index.html?format=text&nodata=404&starttime={}&endtime={}-15&minmag=0&maxmag=10&mindepth=0&maxdepth=900&orderby=time-desc&src=iris&limit=25000&maxlat=85.65&minlat=-85.65&maxlon=180.00&minlon=-180.00&caller=spanevlnk&evid=11524919&zm=1&mt=ter".format(val,val1.split("-")[0]+"-"+val1.split("-")[1]))
                driver.maximize_window()
                driver.execute_script("javascript:showOrExportTable('exportcsv');")
                sleep(5)   
                driver.get("http://www.iris.washington.edu/ieb/index.html?format=text&nodata=404&starttime={}-15&endtime={}-31&minmag=0&maxmag=10&mindepth=0&maxdepth=900&orderby=time-desc&src=iris&limit=25000&maxlat=85.65&minlat=-85.65&maxlon=180.00&minlon=-180.00&caller=spanevlnk&evid=11524919&zm=1&mt=ter".format(val.split("-")[0]+"-"+val.split("-")[1],val1))
                driver.execute_script("javascript:showOrExportTable('exportcsv');")
                sleep(5)
                with open("src/data/csv/IEB_export.csv") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        val = row['Region'].split(",")
                        if len(val) == 2:
                            region = row['Region'].split(",")[0]
                            country = row['Region'].split(",")[1]
                        else:
                            region = row['Region'].split(",")[0]
                            country = str()
                        print(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country)
                        #pg = PostgresClass("admin","admin","localhost",2000,"sismology")
                        #pg.upDelIns('INSERT INTO public.earthquake(dates, times, latitude, longitude, magnitud, region, country)VALUES ("{}", "{}", {}, {}, {}, "{}", "{}");'.format(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country))
                os.remove("src/data/csv/IEB_export.csv")

                with open("src/data/csv/IEB_export (1).csv") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        val = row['Region'].split(",")
                        if len(val) == 2:
                            region = row['Region'].split(",")[0]
                            country = row['Region'].split(",")[1]
                        else:
                            region = row['Region'].split(",")[0]
                            country = str()
                        print(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country)
                        #pg = PostgresClass("admin","admin","localhost",2000,"sismology")
                        #pg.upDelIns('INSERT INTO public.earthquake(dates, times, latitude, longitude, magnitud, region, country)VALUES ("{}", "{}", {}, {}, {}, "{}", "{}");'.format(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country))
                os.remove("src/data/csv/IEB_export (1).csv")
            except Exception as e:
                print(e)
        else:
            monthEnd -= 1
            val1 = str(annoEnd)
            if monthEnd < 10:
                val1 += "-0"+str(monthEnd)
            else:
                val1 += "-"+str(monthEnd)
            try:
                val1 += "-"+str(monthrange(annoInit,monthInit)[1])
                driver.get("http://www.iris.washington.edu/ieb/index.html?format=text&nodata=404&starttime={}&endtime={}-15&minmag=0&maxmag=10&mindepth=0&maxdepth=900&orderby=time-desc&src=iris&limit=25000&maxlat=85.65&minlat=-85.65&maxlon=180.00&minlon=-180.00&caller=spanevlnk&evid=11524919&zm=1&mt=ter".format(val,val1.split("-")[0]+"-"+val1.split("-")[1]+"-15"))
                driver.maximize_window()
                driver.execute_script("javascript:showOrExportTable('exportcsv');")
                sleep(5)   
                driver.get("http://www.iris.washington.edu/ieb/index.html?format=text&nodata=404&starttime={}-15&endtime={}-31&minmag=0&maxmag=10&mindepth=0&maxdepth=900&orderby=time-desc&src=iris&limit=25000&maxlat=85.65&minlat=-85.65&maxlon=180.00&minlon=-180.00&caller=spanevlnk&evid=11524919&zm=1&mt=ter".format(val.split("-")[0]+"-"+val.split("-")[1]+"-15",val1))
                driver.execute_script("javascript:showOrExportTable('exportcsv');")
                sleep(5)
            except Exception as e:
                print(e)
            with open("src/data/csv/IEB_export.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    val = row['Region'].split(",")
                    if len(val) == 2:
                        region = row['Region'].split(",")[0]
                        country = row['Region'].split(",")[1]
                    else:
                        region = row['Region'].split(",")[0]
                        country = str()
                    print(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country)
                    #pg = PostgresClass("admin","admin","localhost",2000,"sismology")
                    #pg.upDelIns('INSERT INTO public.earthquake(dates, times, latitude, longitude, magnitud, region, country)VALUES ("{}", "{}", {}, {}, {}, "{}", "{}");'.format(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country))
            os.remove("src/data/csv/IEB_export.csv")



            with open("src/data/csv/IEB_export (1).csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    val = row['Region'].split(",")
                    if len(val) == 2:
                        region = row['Region'].split(",")[0]
                        country = row['Region'].split(",")[1]
                    else:
                        region = row['Region'].split(",")[0]
                        country = str()
                    print(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country)
                    #pg = PostgresClass("admin","admin","localhost",2000,"sismology")
                    #pg.upDelIns('INSERT INTO public.earthquake(dates, times, latitude, longitude, magnitud, region, country)VALUES ("{}", "{}", {}, {}, {}, "{}", "{}");'.format(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country))
            os.remove("src/data/csv/IEB_export (1).csv")

            monthEnd = 1
            annoEnd += 1      
    driver.close()