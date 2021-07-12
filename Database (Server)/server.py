import sqlite3
import socket
import threading

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNET_MASSAGE = "!DISCONECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handel_client(conn, addr):
    print(addr)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            print(msg_length)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(addr, msg)

            if msg == DISCONNET_MASSAGE:
                connected = False

    conn.close()

def start():
    print("Server is starting...")
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handel_client, args=(conn, addr))
        thread.start()
        print("ative threads : %s"%(threading.activeCount() - 1))

start()



'''
#Connet to database
con_database = sqlite3.connect("Database.db")

cursor = con_database.cursor()

cursor.execute("""CREATE TABLE device(
device_ID INTEGER,
mesange TEXT
)""")
cursor.execute("""INSERT INTO device VALUES (1,'test')""")
cursor.execute("SELECT * FROM device")
print(cursor.fetchall())
con_database.commit()

con_database.close()'''