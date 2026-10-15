from machine import Pin, PWM
import time

# --- Configurare ---

# Pini PWM pentru cele trei canale RGB
red   = PWM(Pin(25), freq=1000, duty=0)
green = PWM(Pin(26), freq=1000, duty=0)
blue  = PWM(Pin(27), freq=1000, duty=0)

DELAY_MS = 10  # cât de lent face fade


def set_color(r, g, b):
    """Setează culoarea LED-ului. Valori 0-1023."""
    red.duty(r)
    green.duty(g)
    blue.duty(b)


def fade(from_color, to_color, steps=255, delay_ms=DELAY_MS):
    """Tranziție lină între două culori (tuple-uri R, G, B)."""
    fr, fg, fb = from_color
    tr, tg, tb = to_color
    for i in range(steps + 1):
        r = fr + (tr - fr) * i // steps
        g = fg + (tg - fg) * i // steps
        b = fb + (tb - fb) * i // steps
        set_color(r, g, b)
        time.sleep_ms(delay_ms)


RED   = (1023, 0, 0)
GREEN = (0, 1023, 0)
BLUE  = (0, 0, 1023)
OFF   = (0, 0, 0)

try:
    while True:
        fade(RED, GREEN)
        fade(GREEN, BLUE)
        fade(BLUE, RED)

except KeyboardInterrupt:
    # La oprire, stinge LED-ul ca să nu rămână aprins
    set_color(0, 0, 0)
    red.deinit()
    green.deinit()
    blue.deinit()
