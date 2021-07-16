import socket
import serial
import threading

HEADER = 64  # Length of number send to set message length. Don't change must be the same for client and server
FORMAT = "utf-8"
DISCONNET_MASSAGE = "!DISCONNECT"

# to connect to database
PORT_CLIENT = 52000
SERVER_CLIENT = "192.168.178.43"  # server to connect to for database
ADDR_CLIENT = (SERVER_CLIENT, PORT_CLIENT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR_CLIENT)

# to open a socket for applications to connect to
PORT = 52001
SERVER = "192.168.178.182"  # IP of the device the gateway runs on
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open server
server.bind(ADDR)

ser = serial.Serial(  # E32 686T20D is connected via USB
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.FIVEBITS,
    timeout=10000
)


def send(msg):  # send a message to the database
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

    print(f"[MESSAGE SEND] {message}")


def gateway_read_LoRA_write_to_database():
    try:  # to safely disconnect from database in case of an error

        print("Gateway started...")

        while True:
            in_come = ser.readline()  # wait till input
            in_come = in_come.decode(FORMAT)
            in_come = in_come.replace("\n", "").replace("\r", "")
            send(in_come)

    finally:
        send(DISCONNET_MASSAGE)
        print("[NO CONNECTION TO DATABASE] send disconnect message")

def handle_client(conn, addr):

    connected = True

    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:  # (can be None)

            msg = conn.recv(len(msg_length)).decode(FORMAT)  # receive message

            if msg == DISCONNET_MASSAGE:
                connected = False

            else:
                ser.write(msg)  # send msg via LoRa
                print(f"[MESSAGE SEND] FROM {addr[0]}")

    conn.close()
    print(f"[CONNECTION CLOSED] {addr[0]}")

def gateway_read_application_write_LoRa():  # applications can send messages witch will be sent by LoRa(module)

    print("Server is starting...")
    server.listen()
    print(f"Server ({ADDR[0]}) is listening on port {ADDR[1]}")

    while True:
        conn, addr = server.accept()  # conn holds the connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[NEW CONNECTION] {addr[0]}")
        print(f"[THREADS USED] {threading.activeCount() - 1}")


threading.Thread(target=gateway_read_LoRA_write_to_database).start()
