import socket
import time
import math

HEADER = 64
PORT = 52000
FORMAT = "utf-8"
DISCONNET_MASSAGE = "!DISCONNECT"
SERVER = "217.160.254.52"
ADDR = (SERVER, PORT)
READ_COMMAND = "!READ"
ID = "0004"  # id of the device


def read(ID: str, client):
    message = (READ_COMMAND + ID).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

    message_length = client.recv(HEADER).decode(FORMAT)
    message = ""
    
    if message_length:
        if int(message_length) < 1440:  # message length is limited to 1440 byts
            message = client.recv(message_length)
        else:
            for i in range(math.ceil(int(message_length)/1440)-1):  # msg_len/1440-1 times: read 1440 byts
                message += client.recv(1440).decode(FORMAT)
                
            byts_left_to_read = int(message_length)-(math.ceil(int(message_length)/1440)-1)*1440
            message +=   client.recv(byts_left_to_read).decode(FORMAT)
            
    
    return(message)


def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)


def run():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)  # connect to server

    try:  # to always disconnect from server

        while True:
            data = read(ID, client)  # get data from database
            
            if data:
                data = " " + data.replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace("(", "")  # reformat
                data = data.split(")")
                data_list = []
                for insert in data:
                    data_list.append(insert.split(" ")[1:4])

                data = data_list
                data = data[:-1]  # to remove extra space at the end
                data = data[::-1]

                date, data = (data[0][0] + " " + data[0][1], data[2])

                software = data[0]  # state of the door by software(0=open, 1=close)
                hardware = data[1]  # state of the door by hardware(0=open, 1=close)

                if software == "1":
                    software = "geschlossen"
                else:
                    software = "offen"

                if hardware == "1":
                    hardware = "geschlossen"
                else:
                    hardware = "offen"

                with open("/var/www/html/H??hnerklappe.html", "w") as html:
                    html.write("""  <!DOCTYPE html>
                                    <html lang="de" dir="ltr">
                                    <head>
                                      <meta charset="utf-8">
                                      <link rel="stylesheet" href="style.css", type="text/css">
                                      <link rel="icon" type="image/png" href="Bilder/icon.png" sizes="96x96">
                                      <title>Sensor Stationen</title>
                                    </head>
                                      <body>
                                        <div id="men??_gesamt">
                                          <a href="index.html"><img src="Bilder/Logo.png" alt="Logo" height="75px" id="men??_logo"></a>
                                        </div>
                                        <div id="seiteninhalt">
                                          <h1>H??hnerklappe</h1>
                                          <br><br><br><br><br><br>
                                          <p class = "Zustand_Klappe">Laut Software: %s</p>
                                          <p class = "Zustand_Klappe">Laut Hardware: %s</p>
                                          <p id="label_letzte_aktualisierung">zuletzt aktual.: %s</p>
                                        </div>
                                      </body>
                                    </html>
                                """ % (software, hardware, date))
                    html.close()
                    
                time.sleep(57)
            time.sleep(3)

    except BrokenPipeError:  # most likely caused by a chance of the public Ip
        print("[BROKEN PIPE] most most likely caused by a chance of the public Ip. Try to fix automatically.")
        print("[TRY TO RECONNECT IN]:")
        for i in range(10):
            print(10 - i)
            time.sleep(1)
        run()
    finally:
        send(DISCONNET_MASSAGE, client)


run()
