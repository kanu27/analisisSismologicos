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
    driver.maximize_window()

    datetimeInit = datetime.datetime.strptime('1970/01/01', '%Y/%m/%d')
    datetimeModific = datetimeInit
    while datetimeInit < datetime.datetime.now():
        datetimeModific += datetime.timedelta(days=+10)
        driver.get("http://www.iris.washington.edu/ieb/index.html?format=text&nodata=404&starttime={}&endtime={}&minmag=0&maxmag=10&mindepth=0&maxdepth=900&orderby=time-desc&src=iris&limit=25000&maxlat=86.99&minlat=-86.99&maxlon=180.00&minlon=-180.00&caller=spanevlnk&evid=11525835&zm=1&mt=ter".format(str(datetimeInit).split(" ")[0],str(datetimeModific).split(" ")[0]))
        sleep(3)
        valor = str(driver.find_element_by_xpath('//*[@id="eventsVisible"]').text)
        valor = valor.replace("(","")
        valor = valor.replace(")","")
        valor = int(valor.split(" ")[0])
        if valor < 25000 and valor > 24000:
            driver.execute_script("javascript:showOrExportTable('exportcsv');")
            datetimeInit = datetimeModific
            datetimeInit += datetime.timedelta(days=+10)
            datetimeModific += datetime.timedelta(days=+10)
            print(str(datetimeInit).split(" ")[0],str(datetimeModific).split(" ")[0])