import sqlite3
import datetime


# A class to handel a sqlite3 based database
class sqlite3_database():
    def __init__(self, name: str):
        # Connet to database
        self.con_database = sqlite3.connect("%s.db"%name)

        self.LENGTH_ID = 4

    def write(self, msg: str):  # msg: "%s%S"%(4 characters for ID, msg)
        msg = msg.strip()  # remove extra spaces
        ID = msg[:self.LENGTH_ID]
        msg = msg[self.LENGTH_ID:]

        date = str(datetime.datetime.now())
        try:  # try to create new table in database in case is the first message from this device
            self.cursor.execute(""" CREATE TABLE ID_%s(
                                    date TEXT,
                                    message TEXT
                                    );"""%ID)
            print(f"[NEW DEVICE IN DATABANK] {ID=}")
        except:
            pass

        # write data to databank
        self.cursor.execute("INSERT INTO ID_%s VALUES('%s', '%s')"%(ID, date, msg))
