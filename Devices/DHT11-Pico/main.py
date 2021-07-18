Authentifizierungs_code_für_Netz = "Zananz"
ID_im_Netz = "0000"
from machine import Pin, UART
import utime

from dht import DHT11, InvalidChecksum

def start_anzeigen():
    led = Pin(25,Pin.OUT)
    led.high()
    utime.sleep(2)
    led.low()
    
start_anzeigen() # um start anzuzeigen und sensor zeit zum starten zu geben
    
uart = UART(0,9600)

pin = Pin(2, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

while 1 :
    try:
        sensor.measure()
        
        temp = sensor.temperature
        feucht = sensor.humidity
        
        uart.write("%s%sT%sL%s"%(Authentifizierungs_code_für_Netz, ID_im_Netz, str(temp), str(feucht)))# T : Temperatu; L : Luftfeuchtigkeit
        
        utime.sleep(600)
    except InvalidChecksum:
        pass
        utime.sleep(2)


