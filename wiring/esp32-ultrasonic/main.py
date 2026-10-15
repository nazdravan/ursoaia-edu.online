from machine import Pin, time_pulse_us
import time

# --- Configurare ---

trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)


def measure_distance_cm(timeout_us=30_000):
    """Returnează distanța în cm sau None dacă nu s-a primit ecou."""
    # Asigură-te că Trig pleacă de la LOW
    trig.value(0)
    time.sleep_us(2)

    # Puls de 10 µs pe Trig
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Așteaptă pulsul HIGH pe Echo și măsoară durata în µs
    duration_us = time_pulse_us(echo, 1, timeout_us)

    if duration_us < 0:
        return None   # timeout — nu s-a întors ecou

    return duration_us * 0.0343 / 2


print("Măsurători HC-SR04. Ctrl+C pentru oprire.\n")

while True:
    try:
        d = measure_distance_cm()
        if d is None:
            print("Out of range")
        else:
            print(f"Distanță: {d:6.2f} cm")
        time.sleep_ms(200)
    except KeyboardInterrupt:
        print("\nStop.")
        break
