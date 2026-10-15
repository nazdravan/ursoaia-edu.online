from machine import Pin, ADC
import time

# --- Configurare ---

ao = ADC(Pin(34))
ao.atten(ADC.ATTN_11DB)          # plaja completă 0-3,3 V

do = Pin(35, Pin.IN)             # ieșire digitală a modulului

# Prag software pentru AO (0-4095). Calibrează în liniștea camerei tale.
ANALOG_THRESHOLD = 2500


def read_sound():
    """Returnează (nivel_analogic, zgomot_detectat)."""
    level = ao.read()
    # DO e active LOW: 0 = sunet peste pragul potențiometrului
    digital_noise = (do.value() == 0)
    return level, digital_noise


print("Senzor de sunet activ. Ctrl+C pentru oprire.\n")

while True:
    try:
        level, noisy = read_sound()
        analog_noise = level > ANALOG_THRESHOLD

        flag = ""
        if noisy or analog_noise:
            flag = "  [ZGOMOT]"

        print(f"AO = {level:4d}   DO = {'LOW (sunet)' if noisy else 'HIGH (liniște)'}{flag}")
        time.sleep_ms(50)
    except KeyboardInterrupt:
        print("\nStop.")
        break
