---
category: ESP32
tags: [Senzor, Temperatură, Umiditate, DHT22, MicroPython]
summary: Citește datele senzorului DHT22 / DHT11 pe un ESP32 și afișează valorile în consola serială la fiecare două secunde.
image: assets/images/projects/esp32/preview-temperature.jpg
---

# Temperatură și umiditate

Citește temperatura și umiditatea de la un senzor DHT22 (sau DHT11) conectat la un ESP32 și afișează valorile în consola serială la fiecare 2 secunde folosind MicroPython.

![Temperatură și umiditate — ESP32 cu senzor DHT22](../../assets/images/projects/esp32/preview-temperature.jpg)

## Descriere

Acest script folosește biblioteca MicroPython integrată `dht` pentru a comunica cu un senzor DHT22 printr-un singur pin de date (GPIO 14). Citește temperatura în grade Celsius, o convertește în Fahrenheit și citește umiditatea relativă, afișând toate trei valorile într-o buclă.

## Cod

```python
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
```

## Conectare

### DHT22 (sau DHT11) la ESP32

```board
Pin DHT22  →  ESP32
---------     -----
VCC (1)    →  3.3V
DATA (2)   →  GPIO 14
GND (4)    →  GND
```

Se recomandă o rezistență pull-up de 10 kΩ între DATA și VCC pentru comunicare fiabilă.

```board
3.3V ──[10kΩ]──┬── GPIO 14
               │
              Pinul DATA al senzorului
```

> **DHT11 vs DHT22:** DHT11 are o precizie mai mică (±2°C, ±5% RH) și un domeniu mai restrâns. DHT22 este mai precis (±0.5°C, ±2–5% RH) și suportă un domeniu mai larg de temperaturi.

### Schema de conectare

[[wokwi:esp32-dht22]]

---

## Referințe

- [ESP32 Based Webserver for Temperature and Humidity Measurement using DHT11 Sensor](https://circuitdigest.com/microcontroller-projects/esp32-webserver-for-temperature-and-humidity-measurement-using-dht11-sensor)
- [ESP32 MicroPython DHT22 Temperature Humidity Sensor](https://newbiely.com/tutorials/esp32-micropython/esp32-micropython-dht22-temperature-humidity-sensor)
