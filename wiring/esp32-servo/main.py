from machine import Pin, PWM
import time

# --- Configurare ---

SERVO_PIN = 13
FREQ = 50          # 50 Hz = perioadă 20 ms (cerută de servo)

# Duty pentru SG90 la rezoluție 10 biți:
#   0°   → puls 0,5 ms  → duty ≈ 26
#   90°  → puls 1,5 ms  → duty ≈ 77
#   180° → puls 2,4 ms  → duty ≈ 123
DUTY_MIN = 26
DUTY_MAX = 123

servo = PWM(Pin(SERVO_PIN), freq=FREQ, duty=0)


def set_angle(angle):
    """Setează unghiul servo-ului între 0 și 180 grade."""
    angle = max(0, min(180, angle))                    # limitează
    duty = DUTY_MIN + (DUTY_MAX - DUTY_MIN) * angle // 180
    servo.duty(duty)


def sweep():
    """Baleiere lentă 0° → 180° → 0°."""
    for a in range(0, 181, 2):
        set_angle(a)
        time.sleep_ms(15)
    for a in range(180, -1, -2):
        set_angle(a)
        time.sleep_ms(15)


try:
    while True:
        sweep()
except KeyboardInterrupt:
    set_angle(90)        # parchează la centru
    time.sleep_ms(500)
    servo.deinit()
