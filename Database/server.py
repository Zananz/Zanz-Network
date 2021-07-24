import socket
import threading
import database
import math

# fixed values
HEADER = 64
PORT = 52000
SERVER = "217.160.254.52"  #IP USED for the socket. To find IP addr automatic socket.gethostbyname(socket.gethostname()) # get IP addr
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNET_MASSAGE = "!DISCONNECT"  # A Massage to quit connection (Server-Client)
KEY = "Zananz"  # A KEY that needs to be at the beginning from every message send from a gateway/application. To enable writing/read to Database
IP_MySQL_SERVER = "127.0.0.1"
USER = "franz"  # username from MySQL
PASSWORD = "Password:type:passwd = 'Püs6/D>sdg$vUhdT50mH%)=|~ß568gtsnf39hvsdZH&9ght09+*~#18hns’'"  # passwd of the user from MySQL
DATABASE_NAME = "Zanz_Network"  # the name of the database
READ_COMMAND = "!READ"  # A command send after the KEY that tells the program to read from Database. (send ID after)

DATABASE = database.MySQL_Database(host=IP_MySQL_SERVER, user=USER, passwd=PASSWORD, database_name=DATABASE_NAME)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handel_client(conn, addr):  # will get called for every client

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)  # receive message

        if msg_length:
            msg_length = int(msg_length)
            msg = ""

            for i in range(math.ceil(int(msg_length) / 1440)):  # message length is limited to 1440 byts
                msg += server.recv(int(msg_length)).decode(FORMAT)

            print(f"[INCOME] {addr[0]} : {msg}")

            if msg == DISCONNET_MASSAGE:
                connected = False
                print(f"[CONNECTION QUIT] {addr[0]}")

            elif msg[:len(KEY)] == KEY:  # check for key
                msg = msg[len(KEY):]  # remove key from message
                DATABASE.write(msg)  # msg hase still ID at the beginning

            elif msg[:len(READ_COMMAND)] == READ_COMMAND:  # check for read command
                ID = msg[len(READ_COMMAND):]  # remove read command

                data = DATABASE.read(ID).encode(FORMAT)  # get all inserts from a device
                data_length = len(data)
                data_length = str(data_length).encode(FORMAT)

                conn.send(data_length)
                conn.send(data)
                print(f"[SEND TO] {addr[0]} DATA FROM ID_{ID}")

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
