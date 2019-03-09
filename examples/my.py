import time
import random

from demo_opts import get_device
from luma.core.render import canvas

def main():
    wifi_level = 2
    device = get_device()
    for _ in range(200):
        wifi_level = random.randint(0, 5)
        with canvas(device) as draw:
            print("Testing display")
            wifi_siganl(device, draw, wifi_level)
            time.sleep(3)

def wifi_siganl(device, draw, wifi_level):
    y_start = 0
    h = 2
    w = 2
    s = 2
    signal_range = 5
    x_start = device.width - ((w + s) * (signal_range + 1) - 1)
    for i in range(0, signal_range):
        if i <= wifi_level:
            color = "white"
        else:
            color = "red"

        x0 = x_start + (w + s)*i
        y0 = y_start
        x1 = x_start + w + (s + w)*i
        y1 = h * i + 1
        draw.rectangle((x0, y0, x1, y1), fill=color)
        text_val = "%s" % wifi_level
        draw.text((0,0), text_val, fill=color)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

