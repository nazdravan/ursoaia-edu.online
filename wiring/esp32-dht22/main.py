from machine import Pin
from time import sleep
import dht

# DHT22 pe GPIO 14
sensor = dht.DHT22(Pin(14))

# Decomentează pentru DHT11
# sensor = dht.DHT11(Pin(14))

while True:
  try:
    sleep(2)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    print('Temperatura: %3.1f C' %temp)
    print('Temperatura: %3.1f F' %temp_f)
    print('Umiditate: %3.1f %%' %hum)
  except OSError as e:
    print('Eroare la citirea senzorului.')
