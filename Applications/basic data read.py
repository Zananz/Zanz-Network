import socket

HEADER = 64
PORT = 52000
FORMAT = "utf-8"
DISCONNET_MASSAGE = "!DISCONNECT"
SERVER = "192.168.178.35"
ADDR = (SERVER, PORT)
READ_COMMAND = "!READ"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)  # connect to server


def read(ID:str):

    message = (READ_COMMAND + ID).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    #print(send_length, message)
    client.send(send_length)
    client.send(message)

    message_length = client.recv(HEADER).decode(FORMAT)
    message = client.recv(int(message_length)).decode(FORMAT)
    return message

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

print(read("0000"))
send(DISCONNET_MASSAGE)