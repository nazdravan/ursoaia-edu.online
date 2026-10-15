try:
  import usocket as socket
except:
  import socket

import network
from machine import Pin
import dht

import esp
esp.osdebug(None)

import gc
gc.collect()

# Configurare
ssid = 'INLOCUIESTE_CU_SSID_TAU'
password = 'INLOCUIESTE_CU_PAROLA_TA'

# Conectare la Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(False)
station.active(True)
station.disconnect()
station.connect(ssid, password)

import time
max_wait = 20
while max_wait > 0:
  if station.isconnected():
    break
  max_wait -= 1
  print('waiting for connection...')
  time.sleep(1)

if station.isconnected():
  print('Connection successful')
  print(station.ifconfig())
else:
  print('Connection failed')
  import sys
  sys.exit()

# Configurare senzor
sensor = dht.DHT11(Pin(4))
#sensor = dht.DHT22(Pin(4))

def read_sensor():
  global temp, hum
  temp = hum = 0
  try:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
      msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))

      # uncomment for Fahrenheit
      #temp = temp * (9/5) + 32.0

      hum = round(hum, 2)
      return(msg)
    else:
      return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')

def web_page():
  html = """<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.2rem; }
    .dht-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>
<body>
  <h2>ESP DHT Server</h2>
  <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i>
    <span class="dht-labels">Temperature</span>
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;C</sup>
  </p>
  <p>
    <i class="fas fa-tint" style="color:#00add6;"></i>
    <span class="dht-labels">Humidity</span>
    <span>"""+str(hum)+"""</span>
    <sup class="units">%</sup>
  </p>
</body>
</html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    conn, addr = s.accept()
    conn.settimeout(5)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    sensor_readings = read_sensor()
    print(sensor_readings)
    response = web_page()
    response_bytes = response.encode('utf-8')
    conn.send(b'HTTP/1.1 200 OK\r\n')
    conn.send(b'Content-Type: text/html\r\n')
    conn.send(b'Content-Length: ' + str(len(response_bytes)).encode() + b'\r\n')
    conn.send(b'Connection: close\r\n\r\n')
    conn.sendall(response_bytes)
  except Exception as e:
    print('Error: %s' % str(e))
  finally:
    conn.close()
