import os
import datetime
import time

time.sleep(60)

while True:
    time_now = str(datetime.datetime.now().time()).split(":")
    if time_now[0] == "03" and time_now[1] == "57":
        os.system("reboot")
    time.sleep(58)
