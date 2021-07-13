# a class to handle the Database
import datetime

import mysql.connector

class MySQL_Database():
    def __init__(self, host:str, user:str, passwd:str, database_name:str):

        self.db = mysql.connector.connect(   # connect to database
            host = host,
            user = user,
            passwd = passwd,
            database = database_name
        )

    def write(self, msg:str):

        ID = msg[:4] # fixes the ID length to an 4 symbols long str
        msg = msg[4:]

        cursor = self.db.cursor()

        try: #T try to create an new table in case of a first commit from a device
            cursor.execute(f"""CREATE TABLE ID_{ID}(
            date CHAR(19),
            message VARCHAR(100)  
            );""")
        except:
            print(Exception)
        print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print(msg)
        cursor.execute(""" INSERT INTO ID_%s (date, message) VALUES (
                            '%s',
                            '%s')
                            """%(ID, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), msg))
        self.db.commit()
        cursor.close()



