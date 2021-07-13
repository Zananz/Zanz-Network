import socket
import threading
import database

# fixed values
HEADER = 64
PORT = 52000
SERVER = socket.gethostbyname(socket.gethostname()) # get IP addr
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNET_MASSAGE = "!DISCONNECT"  # A Massage to quit connection (Server-Client)
KEY = "Zananz" # A KEY that needs to be at the beginning from every messang send from a gateway. To enable writing to Database
LENGTH_KEY = len(KEY) # needed to check for the key
IP_MySQL_SERVER = ""
USER = "" # username from MySQL
PASSWORD = "" # passwd ot the user from MySQL
DATABASE_NAME = "" # the name of the database

DATABASE = database.MySQL_Database(host=IP_MySQL_SERVER, user=USER, passwd=PASSWORD, database_name=DATABASE_NAME)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handel_client(conn, addr):  # will get called for every client

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)  # receive message

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[INCOME] {addr[0]} : {msg}")

            if msg == DISCONNET_MASSAGE:
                connected = False
                print(f"[CONNECTION QUIT] {addr[0]}")

            elif msg[:LENGTH_KEY] == KEY: # check for key
                msg = msg[LENGTH_KEY:] # remove key from message
                DATABASE.write(msg) # msg hase still ID at the beginning
    conn.close()


def start():
    print("Server is starting...")
    server.listen()
    print(f"Server ({ADDR[0]}) is listening on port {ADDR[1]}")
    while True:
        conn, addr = server.accept()  # conn holds the connection
        thread = threading.Thread(target=handel_client, args=(conn, addr))
        thread.start()
        print(f"[NEW CONNECTION] {addr[0]}")
        print(f"[THREADS USED] {threading.activeCount() - 1}")


start()