import os
import datetime
import time

time.sleep(60)

while True:
    time_now = str(datetime.datetime.now().time()).split(":")
    if time_now[0] == "04" and time_now[1] == "00":
        os.system("sudo reboot")
    time.sleep(58)
