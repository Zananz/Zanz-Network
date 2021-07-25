import socket
import serial
import time

HEADER = 64 # Length of number send to set message length. Don't change must be the same for client and server
PORT = 52000
FORMAT = "utf-8"
DISCONNET_MASSAGE = "!DISCONNECT"
SERVER = "192.168.178.35"
ADDR = (SERVER, PORT)

ser = serial.Serial( # E32 686T20D is connected via USB
     port='/dev/ttyACM0',
     baudrate = 9600,
     parity=serial.PARITY_NONE,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.FIVEBITS,
     timeout=10000
)


def send(msg, client): # send a message to the database
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    
    client.send(send_length)
    client.send(message)
    
    print(f"[MESSAGE SEND] {message}")

def run():
    try: #to safely disconnect from database in case of an error

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)

        print("Gateway started...")

        while True:

            in_come = ser.readline() # wait till input
            print(in_come)
            in_come = in_come.decode()
            print(in_come)
            in_come = in_come.replace("\n", "").replace("\r", "")
            print(in_come)
            send(in_come, client)

    except BrokenPipeError:  # most likely caused by a chance of the public Ip
        print("[BROKEN PIPE] most most likely caused by a chance of the public Ip. Try to fix automatically.")
        print("[TRY TO RECONNECT IN]:")
        for i in range(5):
            print(5 - i)
            time.sleep(1)
        run()

    finally:
        send(DISCONNET_MASSAGE)
    