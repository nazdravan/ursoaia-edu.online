# Display OLED 128x64 I2C (SSD1306) pe ESP32 cu driverul ssd1306 din micropython-lib
# Conectare: VCC -> 3V3, GND -> GND, SCL -> GPIO 22, SDA -> GPIO 21
# Instalare driver: mpremote mip install ssd1306  (sau Thonny -> Manage packages)
from machine import Pin, I2C
from time import sleep
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
print("Dispozitive I2C:", [hex(a) for a in i2c.scan()])  # trebuie să apară 0x3c

oled = ssd1306.SSD1306_I2C(128, 64, i2c)


def demo_text():
    oled.fill(0)
    oled.text("Cerc de", 0, 0)
    oled.text("informatica", 0, 10)
    oled.text("Salut, ESP32!", 0, 30)
    oled.text("2025", 0, 50)
    oled.show()


def demo_shapes():
    oled.fill(0)
    oled.rect(0, 0, 40, 30, 1)            # dreptunghi
    oled.fill_rect(45, 0, 40, 30, 1)      # dreptunghi plin
    oled.ellipse(108, 15, 14, 14, 1)      # cerc (MicroPython 1.20+)
    oled.line(0, 63, 127, 34, 1)          # linie
    oled.show()


def demo_counter():
    for i in range(0, 101, 5):
        oled.fill(0)
        oled.text("Incarcare...", 0, 0)
        oled.text("{:3d}%".format(i), 48, 24)
        oled.rect(0, 52, 128, 12, 1)                  # contur bară
        oled.fill_rect(2, 54, i * 124 // 100, 8, 1)   # bara
        oled.show()
        sleep(0.1)


while True:
    demo_text()
    sleep(2)
    demo_shapes()
    sleep(2)
    demo_counter()
    sleep(1)
