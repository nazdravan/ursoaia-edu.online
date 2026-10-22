---
title: ESP32
overview: true
tags: [ESP32, IoT, MicroPython, Wi-Fi]
summary: ESP32 projects with MicroPython — Wi-Fi, sensors, web servers, and IoT prototypes.
---

# ESP32 Projects

The ESP32 is a microcontroller with **built-in Wi-Fi and Bluetooth**, ideal for IoT projects, automation, and small web servers. It runs MicroPython natively — Python syntax applies directly, no compilation needed.

## Available projects

### [LED Blink](led_blink.md)

The "Hello World" of embedded systems — toggles the on-board LED (GPIO 2) using MicroPython. Includes a **LED chaser** example across consecutive pins.

- **Components:** ESP32, external LED (optional), 220 Ω resistor
- **Concepts:** GPIO, lifecycle of a MicroPython script
- **Difficulty:** beginner

---

### [RGB LED](rgb_led.md)

Drive an RGB LED with three **PWM** channels on the ESP32 — smooth fading between red, green, and blue, plus fixed-color and random-color examples. MicroPython code.

- **Components:** ESP32, common-cathode RGB LED, 3× 220 Ω resistor
- **Concepts:** 10-bit PWM, `duty()`, additive color mixing
- **Difficulty:** beginner

---

### [Servo](servo.md)

Drive an **SG90 servo** to a precise angle between 0° and 180° using PWM at 50 Hz. Includes a slow sweep, manual end-stop calibration, and power-supply tips to avoid resets.

- **Components:** ESP32, SG90 servo, 5 V supply (Vin or external)
- **Concepts:** 50 Hz PWM, angle → duty mapping, mechanical calibration
- **Difficulty:** beginner-intermediate

---

### [Joystick](joystick.md)

Read an analog joystick on **ADC1** (GPIO 34, 35) plus the push button — and turn the two axes into a direction (left / right / up / down) with a dead zone. Also includes a proportional −100…+100 mapping for games.

- **Components:** ESP32, KY-023 joystick module, jumper wires
- **Concepts:** 12-bit ADC, attenuation, dead zone, ADC1 vs ADC2 with Wi-Fi
- **Difficulty:** beginner-intermediate

---

### [Ultrasonic Sensor](ultrasonic.md)

Measure distance to objects with the **HC-SR04** — a 10 µs pulse on Trig, time the echo on Echo, compute centimetres. Includes the mandatory voltage divider for the 3.3 V ESP32, a median filter, and a proximity alarm.

- **Components:** ESP32, HC-SR04 (or HC-SR04P), 1 kΩ + 2 kΩ resistors
- **Concepts:** `time_pulse_us`, 5 V vs 3.3 V, voltage divider, median filter
- **Difficulty:** beginner-intermediate

---

### [Sound Sensor](sound_sensor.md)

Detect sound with a **KY-038** module (electret mic + LM393) — read both the analog level (AO) and the tunable-threshold digital output (DO). Examples: clap-to-LED and a clap-clap toggle.

- **Components:** ESP32, KY-038 module, jumper wires
- **Concepts:** LM393 comparator, ADC vs digital input, threshold calibration, sound debouncing
- **Difficulty:** beginner-intermediate

---

### [Temperature & Humidity](temperature.md)

Reads a **DHT22** (or DHT11) sensor and prints values to the serial console every 2 seconds.

- **Components:** ESP32, DHT22/DHT11, 10 kΩ pull-up resistor
- **Concepts:** 1-wire communication, exception handling, output formatting
- **Difficulty:** beginner-intermediate

---

### [Temperature Web Server](temperature_web.md)

Combines ESP32's Wi-Fi with the DHT22 sensor — serves a **styled HTML page** with live readings, accessible from any browser on the same network.

- **Components:** ESP32, DHT22, Wi-Fi connection
- **Concepts:** TCP socket, basic HTTP, HTML string formatting
- **Difficulty:** intermediate

---

### [ESP-NOW Messaging](esp_now.md)

Two ESP32 boards exchange messages **directly, with no router and no internet**, using the ESP-NOW protocol. Sub-10 ms latency, up to 250 bytes per packet.

- **Components:** 2× ESP32 (that's it)
- **Concepts:** ESP-NOW peer-to-peer, MAC addressing, Wi-Fi channels, broadcast vs unicast
- **Difficulty:** intermediate

---

### [128x64 I2C OLED Display](oled_display.md)

Show text and graphics on an SSD1306 OLED display with MicroPython — first using only the firmware's `machine.I2C` and `framebuf`, then with the **ssd1306** driver from micropython-lib.

- **Components:** ESP32, 0.96" 128x64 I2C OLED display
- **Concepts:** I2C, `framebuf`, screen buffer, `mip install`
- **Difficulty:** beginner-intermediate

---

## Why ESP32?

| Feature | Detail |
|---------|--------|
| **CPU** | Dual-core 240 MHz (much faster than Arduino Uno) |
| **Memory** | 520 KB RAM, 4 MB Flash |
| **Wi-Fi** | 802.11 b/g/n built-in |
| **Bluetooth** | Classic + BLE |
| **I/O pins** | 30+ GPIO, ADC, DAC, PWM |
| **Price** | ~5–10 € per board |

## Tools

- **[Thonny](https://thonny.org/)** — recommended IDE for MicroPython (ESP32 support built-in)
- **[esptool.py](https://github.com/espressif/esptool)** — flash MicroPython firmware to ESP32
- **[MicroPython firmware](https://micropython.org/download/esp32/)** — get the generic ESP32 build

## Where to start

1. **Flash MicroPython** onto your ESP32 with `esptool.py`
2. Connect via Thonny (pick "MicroPython (ESP32)" interpreter)
3. Run [LED Blink](led_blink.md) first to verify your setup
4. Continue with the temperature sensor, then the web server

!!! tip "Coming from Arduino?"
    Syntax is different — Python instead of C++ — but the concepts are the same (GPIO, sleep, interrupt, communication). The MicroPython advantage: **no compile step** on every change; code runs directly.

!!! note "ESP32 vs ESP8266"
    ESP8266 is older and more limited (only Wi-Fi, less RAM). For new projects we recommend ESP32.
