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

# has to stand at the beginning of every message

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)  # connect to server


def read(ID: str):
    message = (READ_COMMAND + ID).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

    message_length = client.recv(HEADER).decode(FORMAT)
    message = ""
    for i in range(math.ceil(int(message_length) / 1440)):
        message += client.recv(int(message_length)).decode(FORMAT)

    return message


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)


try:  # to always disconnect from server

    while True:
        data = read(ID)  # get data from database

        data = " " + data.replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace("(","")  # reformat
        data = data.split(")")
        data_list = []
        for insert in data:
            data_list.append(insert.split(" ")[1:4])

        data = data_list
        data = data[:-1]  # to remove extra space at the end
        data = data[::-1]

        date, data = (str(data[0][0]) + " " + str(data[0][1]) , data[2])

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

        with open("/var/www/html/Hühnerklappe.html", "w") as html:
            html.write("""  <!DOCTYPE html>
                            <html lang="de" dir="ltr">
                            <head>
                              <meta charset="utf-8">
                              <link rel="stylesheet" href="style.css", type="text/css">
                              <link rel="icon" type="image/png" href="Bilder/icon.png" sizes="96x96">
                              <title>Sensor Stationen</title>
                            </head>
                              <body>
                                <div id="menü_gesamt">
                                  <a href="index.html"><img src="Bilder/Logo.png" alt="Logo" height="75px" id="menü_logo"></a>
                                </div>
                                <div id="seiteninhalt">
                                  <h1>Hühnerklappe</h1>
                                  <br><br><br><br><br><br>
                                  <p class = "Zustand_Klappe">Laut Software: %s</p>
                                  <p class = "Zustand_Klappe">Laut Hardware: %s</p>
                                  <p id="label_letzte_aktualisierung">zuletzt aktual.: %s</p>
                                </div>
                              </body>
                            </html>
                        """%(software, hardware, date))
        time.sleep(600)

finally:
    send(DISCONNET_MASSAGE)
