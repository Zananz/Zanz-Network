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
ID = "0000"  # id of the device

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
    for i in range(math.ceil(int(message_length)/1440)):
        message += client.recv(int(message_length)).decode(FORMAT)
    
    print(message)
    
    return(message)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)


try:  # to alwas disconect from server

    while True:
        data = read(ID)  # get data from database
        print(len(data))
        data = " " + data.replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace("(", "")  # reformat
        data = data.split(")")
        data_list = []
        for insert in data:
            data_list.append(insert.split(" ")[1:4])

        data = data_list
        data = data[:-1]  # to remove extra space at the end

        last_data = data[-1]

        date = last_data[0].replace("-",".")+" "+last_data[1]
        temperature, humidity = last_data[2].replace("T","").split("L")

        with open("/var/www/html/Luft Station.html", "w") as html:
            print(1)
            html.write("""<!DOCTYPE html>
                            <html lang=de dir="ltr">
                              <head>
                                <meta charset="utf-8">
                                <link rel="stylesheet" href="style.css", type="text/css">
                                <link rel="icon" type="image/png" href="Bilder/icon.png" sizes="96x96">
                                <title>Wetter</title>
                              </head>
                              <body>
                                <div id="menü_gesamt">
                                <a href="index.html"><img src="Bilder/Logo.png" alt="Logo" height="75px" id="menü_logo"></a>
                                <table id="menü_tabelle">
                                  <tr>
                                    <td class="menü_tabellen_spalte"><a class ="menü_tabellen_element" href="#">AKTUELL</td>
                                    <td class="menü_tabellen_spalte"><a class ="menü_tabellen_element" href="Vergangene Messungen.html">VERGANGENE</td>
                                  </tr>
                                </table>
                              </div>
                              <div id="seiteninhalt">
                                <h1>Aktuell</h1>
                                <p id="temperatur_luft">%s°</p>
                                <p id="luftfeuchtigkeit">@%s%%</p>
                                <p id="label_letzte_aktualisierung">zuletzt aktual.: %s</p>
                              </div>
                              </body>
                            </html>"""%(temperature, round(float(humidity)), date))
            html.close()
            
        data = data[::-1]

        data_all_str = ""  # to write into html later

        for insert in data:
            date = insert[0].replace("-", ".") + " " + insert[1]
            temperature, humidity = insert[2].replace("T", "").split("L")

            data_all_str += """<tr class="h24_tabelle_reihe">
                                    <td class = "h24_tabelle_datum">%s</td>
                                    <td class = "h24_tabelle_werte">%s°&nbsp;%s%%</td>
                                </tr>"""%(date, temperature, round(float(humidity)))

        with open("/var/www/html/Vergangene Messungen.html", "w") as html:
            html.write("""
                <!DOCTYPE html>
                <html lang=de dir="ltr">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" href="style.css", type="text/css">
                    <link rel="icon" type="image/png" href="Bilder/icon.png" sizes="96x96">
                    <title>Tepmeratur</title>
    
                  </head>
                  <body>
                    <div id="menü_gesamt">
                    <a href="index.html"><img src="Bilder/Logo.png" alt="Logo" height="75px" id="menü_logo"></a>
                    <table id="menü_tabelle">
                      <tr>
                        <td class="menü_tabellen_spalte"><a class ="menü_tabellen_element" href="Luft Station.html">AKTUELL</td>
                        <td class="menü_tabellen_spalte"><a class ="menü_tabellen_element" href="#">VERGANGENE</td>
    
                      </tr>
                    </table>
                  </div>
                  <div id="seiteninhalt">
                    <h1>VERGANGENE MESSUNGEN</h1>
                    <table id = "h24_tabelle">
                      %s
                    </table>
                  </div>
                  </body>
                </html>""" % data_all_str)

            html.close()
        time.sleep(600)

finally:
    send(DISCONNET_MASSAGE)
    print("Disconnected")
