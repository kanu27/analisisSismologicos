import csv
from helper.database.postgres import PostgresClass

if __name__ == "__main__":
    with open("src/data/sismosMundiales.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            val = row['Region'].split(",")
            if len(val) == 2:
                region = row['Region'].split(",")[0]
                country = row['Region'].split(",")[1]
            else:
                region = row['Region'].split(",")[0]
                country = None
            pg = PostgresClass("admin","admin","localhost",2000,"sismology")
            pg.upDelIns("INSERT INTO public.earthquake(dates, times, latitude, longitude, magnitud, region, country)VALUES ('{}', '{}', {}, {}, {}, '{}', '{}');".format(row['Year'] +"/"+ row['Month'] +"/"+ row['Day'], row['Time'], row['Lat'], row['Lon'], row['Mag'],region,country))
