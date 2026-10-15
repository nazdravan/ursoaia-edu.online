import machine
import time

# LED extern pe GPIO 4 (prin 220 Ω), ca în schema de conectare
led = machine.Pin(4, machine.Pin.OUT)

while True:
    led.value(1) # Aprinde LED-ul
    time.sleep(1)
    led.value(0) # Stinge LED-ul
    time.sleep(1)
