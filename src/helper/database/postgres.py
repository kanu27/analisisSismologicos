"""
development date: 23/01/2022
Author name: Kevin Ponce
author information:
    url: www.kanu.cl
    email: kanu.ponce@gmail.com
"""
import psycopg2
from helper.services.log import Log

class PostgresClass():
    def __init__(self,
                 vuser: str,
                 vpassword: str,
                 vurl: str = 'localhost',
                 vport: int = 5432,
                 vdataBase: str = None):
        self.user = vuser
        self.password = vpassword
        self.url = vurl
        self.port = vport
        self.dataBase = vdataBase
        self.conn = None

    def conectionOn(self):
        """
        Init conection postgres
        """
        try:
            self.conn = psycopg2.connect(host=self.url,
                                         dbname=self.dataBase,
                                         user=self.user,
                                         password=self.password,
                                         port=self.port)
        except psycopg2.DatabaseError as e:
            Log("ERROR BD: " + str(e),"error","PostgresClass","openConection")
            Log.console()
        except Exception as e:
            Log("ERROR UNKNOWN: " + str(e),"error","PostgresClass","openConection")
            Log.console()

    def conectionOff(self):
        """
        Close conection postgres
        """
        try:
            self.conn.close()
        except psycopg2.DatabaseError as e:
            Log("ERROR BD: " + str(e),"error","PostgresClass","openConection")
            Log.console()
        except Exception as e:
            Log("ERROR UNKNOWN: " + str(e),"error","PostgresClass","openConection")
            Log.console()


    def dataBaseManipulation(self,
                             action: str,
                             nameBd: str,
                             alterCommant: str = ""):
        """
        CREATE,DROP or ALTER DATABASE\n
        example:\n
        ('CREATE','ANIMAL','')\n
        ('ALTER','ANIMAL','RENAME TO PERSON')
        - `@action = (CREATE,ALTER,DROP)`
        - `@nameBd = name database`
        - `@alterCommant = only if action is alter`
        """
        self.conectionOn()
        cur = self.conn.cursor()
        try:
            self.conn.autocommit = True
            query = action + " DATABASE " + nameBd
            if alterCommant != '':
                query += " "+alterCommant
            query += ";"
            query = query
            cur.execute(query)
        except psycopg2.DatabaseError as e:
            Log("ERROR BD: " + str(e),"error","PostgresClass","openConection")
            Log.console()
        except Exception as e:
            Log("ERROR UNKNOWN: " + str(e),"error","PostgresClass","openConection")
            Log.console()
        finally:
            if self.conn is not None:
                cur.close()
                self.conectionOff()

    def tableManipulation(self,
                          action: str,
                          table: str,
                          alterCommant: str = "",
                          cascadeDrop: bool = False):
        """
        CREATE,DROP or ALTER  TABLE\n
        example:\n 
        ('CREATE','VENDORS(VENDORID SERIAL PRIMARY KEY,VENDORNAME VARCHAR(255) NOT NULL)')\n
        ('DROP','VENDORS',True)
        - `@action = (CREATE,ALTER,DROP)`
        - `@nameBd = name table or table`
        - `@alterCommant = only if action is alter`
        - `@cascadeDrop = only if action is drop(True or False)`
        """
        self.conectionOn()
        cur = self.conn.cursor()
        query = str()
        try:
            action = action.upper()
            self.conn.autocommit = True
            if action == "CREATE":
                query = "CREATE TABLE IF NOT EXISTS " + table
            elif action == "ALTER":
                query = "ALTER TABLE " + table + " " + alterCommant
            else:
                query = "DROP TABLE IF EXISTS " + table
                if cascadeDrop == True:
                    query += " CASCADE"
            query += ";"
            cur.execute(query)
        except psycopg2.DatabaseError as e:
            Log("ERROR BD: " + str(e),"error","PostgresClass","openConection")
            Log.console()
        except Exception as e:
            Log("ERROR UNKNOWN: " + str(e),"error","PostgresClass","openConection")
            Log.console()
        finally:
            if self.conn is not None:
                cur.close()
                self.conectionOff()

    def select(self, query: str):
        """
        SELECT DATA\n
        example:\n 
        "SELECT * FROM person ORDER BY id ASC;"\n
        - `@query = select complete to execute`
        """
        self.conectionOn()
        cur = self.conn.cursor()
        try:
            cur.execute(query)
            return cur.fetchall()
        except psycopg2.DatabaseError as e:
            Log("ERROR BD: " + str(e),"error","PostgresClass","openConection")
            Log.console()
        except Exception as e:
            Log("ERROR UNKNOWN: " + str(e),"error","PostgresClass","openConection")
            Log.console()
        finally:
            if self.conn is not None:
                cur.close()
                self.conectionOff()

    def upDelIns(self, query):
        """
        INSERT,UPDATE or DELETE DATA\n
        example:\n 
        "INSERT INTO person(id, name, lastname) VALUES (1, 'Kevin', 'Ponce');"\n
        "UPDATE person SET lastname='Aguilera' WHERE id=1;"\n
        - `@query = query complete to execute`
        """
        self.conectionOn()
        cur = self.conn.cursor()
        try:
            self.conn.autocommit = True
            cur.execute(query)
            updatedRows = cur.rowcount
            return updatedRows
        except psycopg2.DatabaseError as e:            
            Log.console(Log("ERROR BD: " + str(e),"error","PostgresClass","openConection"))
        except Exception as e:            
            Log.console(Log("ERROR UNKNOWN: " + str(e),"error","PostgresClass","openConection"))
        finally:
            if self.conn is not None:
                cur.close()
                self.conectionOff()
