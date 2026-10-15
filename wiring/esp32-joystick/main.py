from machine import Pin, ADC
import time

# --- Configurare ---

vrx = ADC(Pin(34))
vry = ADC(Pin(35))
vrx.atten(ADC.ATTN_11DB)   # plaja completă 0-3,3 V
vry.atten(ADC.ATTN_11DB)

button = Pin(32, Pin.IN, Pin.PULL_UP)   # active LOW: 0 = apăsat

# Praguri pentru zona moartă (centru ~2048, ±35%)
DEAD_LOW = 1300
DEAD_HIGH = 2800


def read_direction():
    """Returnează 'STOP' / 'STANGA' / 'DREAPTA' / 'SUS' / 'JOS'."""
    x = vrx.read()
    y = vry.read()

    x_out = x < DEAD_LOW or x > DEAD_HIGH
    y_out = y < DEAD_LOW or y > DEAD_HIGH

    if not x_out and not y_out:
        return "STOP", x, y

    # Câștigă axa cu deflecție mai mare față de centru
    dx = x - 2048
    dy = y - 2048
    if abs(dx) >= abs(dy):
        return ("STANGA" if x < DEAD_LOW else "DREAPTA"), x, y
    else:
        return ("SUS" if y < DEAD_LOW else "JOS"), x, y


print("Mișcă joystick-ul. Ctrl+C pentru oprire.\n")

last_dir = None
while True:
    direction, x, y = read_direction()
    pressed = button.value() == 0   # 0 = apăsat

    # Afișează doar când se schimbă direcția sau butonul
    if direction != last_dir or pressed:
        print(f"X={x:4d}  Y={y:4d}  →  {direction}{'  [BUTON]' if pressed else ''}")
        last_dir = direction

    time.sleep_ms(50)
