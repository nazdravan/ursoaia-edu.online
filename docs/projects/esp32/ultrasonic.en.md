---
category: ESP32
tags: [Ultrasonic, HC-SR04, Distance, Sensor, MicroPython]
summary: Measure distance to objects with HC-SR04 and the ESP32 — fire a 40 kHz pulse and time the echo to compute distance in cm.
image: assets/images/projects/esp32/preview-ultrasonic.jpg
---

# Ultrasonic sensor

HC-SR04 is the go-to sensor for "how far is the object in front of me?". You find it in obstacle-avoiding robots, parking systems, and presence alarms. Here we wire it to the ESP32 and read the distance in MicroPython using `machine.time_pulse_us`.

![HC-SR04 ultrasonic sensor wired to ESP32](../../assets/images/projects/esp32/preview-ultrasonic.jpg)

## Description

The HC-SR04 has 4 pins: `VCC`, `Trig`, `Echo`, `GND`. The principle is the same as bats use:

1. The ESP32 pulses `Trig` `HIGH` for **10 microseconds**.
2. The sensor emits 8 cycles of ultrasound at **40 kHz** (inaudible to humans).
3. When the ultrasound hits an obstacle it bounces back as an echo.
4. The `Echo` pin stays `HIGH` for exactly as long as the sound's round-trip takes.
5. The ESP32 times the pulse with `time_pulse_us` and computes the distance.

### Distance math

Sound travels through air at ~**343 m/s** = 0.0343 cm/µs. Since the measured time is the round trip, we divide by 2:

```
distance [cm] = duration [µs] × 0.0343 / 2
```

Or equivalently: `duration / 58.3`.

**Useful range:** 2 cm – 400 cm, ~3 mm accuracy.

## Components

| Component | Quantity |
|-----------|----------|
| ESP32 board (DevKit V1) | 1 |
| HC-SR04 module (or HC-SR04**P** — the 3.3 V variant) | 1 |
| 1 kΩ resistor | 1 (only with the classic HC-SR04) |
| 2 kΩ resistor | 1 (only with the classic HC-SR04) |
| F-M jumper wires | 4 |

!!! warning "HC-SR04 outputs 5 V on Echo — the ESP32 is 3.3 V"
    The **classic HC-SR04** is powered at 5 V and drives **5 V** on its Echo pin. The ESP32's GPIOs are not 5 V tolerant — wiring it directly can damage the pin over time. Two options:

    - **Recommended:** use the **HC-SR04P** (or HC-SR04+) which runs at 3.3 V — no resistors, direct connection.
    - **With the classic HC-SR04:** put a **voltage divider** on Echo (1 kΩ + 2 kΩ) to bring 5 V → 3.3 V. Trig can stay connected directly, since the ESP32 drives 3.3 V and the HC-SR04 reads it as HIGH.

## Wiring

| Sensor pin | ESP32 |
|------------|-------|
| VCC | Vin / 5V (classic HC-SR04) **or** 3.3V (HC-SR04P) |
| GND | GND |
| Trig | GPIO 5 |
| Echo | GPIO 18 (through a voltage divider, see below) |

### Voltage divider on Echo (classic HC-SR04)

[[wokwi:esp32-ultrasonic]]

```board
   Echo (5 V) ──[ 1 kΩ ]──┬── GPIO 18 (3.3 V)
                           │
                          [ 2 kΩ ]
                           │
                          GND
```

`V_out = V_in × 2 / (1 + 2) = 5 × 2/3 ≈ 3.3 V` — exactly the ESP32 threshold.

### Full schematic

```board
    ESP32                   HC-SR04
    Vin / 5V ────────── VCC
    GND ────────────── GND
    GPIO 5 ──────────── Trig
    GPIO 18 ◄─[1 kΩ]─── Echo
                    └──[2 kΩ]──── GND
```

## Code

```python
from machine import Pin, time_pulse_us
import time

# --- Setup ---

trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)


def measure_distance_cm(timeout_us=30_000):
    """Return the distance in cm or None if no echo came back."""
    # Make sure Trig starts LOW
    trig.value(0)
    time.sleep_us(2)

    # 10 µs pulse on Trig
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Wait for the HIGH pulse on Echo and measure its duration in µs
    duration_us = time_pulse_us(echo, 1, timeout_us)

    if duration_us < 0:
        return None   # timeout — no echo

    return duration_us * 0.0343 / 2


print("HC-SR04 readings. Ctrl+C to stop.\n")

while True:
    try:
        d = measure_distance_cm()
        if d is None:
            print("Out of range")
        else:
            print(f"Distance: {d:6.2f} cm")
        time.sleep_ms(200)
    except KeyboardInterrupt:
        print("\nStop.")
        break
```

## Run the script

1. Plug the ESP32 into USB and assemble the circuit (mind the voltage divider).
2. In Thonny paste the code and press **Run** (F5).
3. Wave your hand in front of the sensor. The console shows values like:

```
HC-SR04 readings. Ctrl+C to stop.

Distance:  37.42 cm
Distance:  22.18 cm
Distance:   8.74 cm
Distance:   3.12 cm
Out of range
```

For a stable reading, average several measurements (see example below).

## Example: median filter

The sensor occasionally returns outliers (echoes bouncing off multiple surfaces). A simple filter — the median of 5 readings — kills most of them:

```python
def measure_smoothed(samples=5):
    """Median of `samples` readings — robust to outliers."""
    readings = []
    for _ in range(samples):
        d = measure_distance_cm()
        if d is not None:
            readings.append(d)
        time.sleep_ms(40)   # >= 60 ms is ideal
    if not readings:
        return None
    readings.sort()
    return readings[len(readings) // 2]
```

## Example: proximity LED alarm

Light the onboard LED (GPIO 2) when something gets closer than 15 cm:

```python
from machine import Pin, time_pulse_us
import time

trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
led = Pin(2, Pin.OUT)

THRESHOLD_CM = 15

def distance_cm():
    trig.value(0); time.sleep_us(2)
    trig.value(1); time.sleep_us(10); trig.value(0)
    d = time_pulse_us(echo, 1, 30_000)
    return None if d < 0 else d * 0.0343 / 2

while True:
    d = distance_cm()
    led.value(1 if d is not None and d < THRESHOLD_CM else 0)
    time.sleep_ms(100)
```

## Troubleshooting

??? question "`time_pulse_us` always returns a negative value (timeout)"
    - Check the **Echo** wire — should land on GPIO 18, through the voltage divider if you have a classic HC-SR04.
    - The sensor isn't getting enough current — try powering it from **Vin** (5 V) instead of 3.3V.
    - The obstacle is closer than 2 cm or farther than 4 m — outside the useful range.
    - The obstacle's surface absorbs sound (clothes, foam) — test with a book or wall.

??? question "Readings jump around (e.g. 30 cm, 12 cm, 28 cm)"
    - Use a **median of 5 readings** (example above) — kills most outliers.
    - Leave at least **60 ms** between measurements so previous echoes can die down.
    - Avoid pointing the sensor at **reflective walls** (glass, polished metal) which create multipath echoes.

??? question "ESP32 resets after a few readings"
    - Weak USB power. Use a quality USB data cable or an external supply on Vin.

??? question "How do I know if I have HC-SR04 or HC-SR04P?"
    - Read the silkscreen on the board. The HC-SR04**P** usually has a smaller chip and is missing the large silver capacitor (regulator) present on the classic version. If unsure, **add the divider** — it doesn't hurt anything and it protects you from 5 V.

## Extension ideas

- **Parking system:** a passive buzzer that beeps faster as you get closer — combine with a PWM pin (see [Servo](servo.md)) which sets the `tone` frequency.
- **180° radar:** mount the HC-SR04 on a [servo](servo.md) and sweep — show readings on an LCD or stream them to the PC.
- **Water-level indicator:** measure the distance to the water surface in a tank.
- **Wireless telemetry:** [ESP-NOW](esp_now.md) can ship the distance to a master board that logs the data.

---

## References

- [MicroPython — `machine.time_pulse_us`](https://docs.micropython.org/en/latest/library/machine.html#machine.time_pulse_us)
- [HC-SR04 datasheet (Cytron)](https://www.cytron.io/p-hc-sr04)
- [Random Nerd Tutorials — ESP32 Ultrasonic Sensor (MicroPython)](https://randomnerdtutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/)
