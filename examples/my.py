import time
import datetime

from demo_opts import get_device
from luma.core.render import canvas

def main():
    device = get_device()
    y_start = 0
    signal_range = 30
    h = 2
    w = 2
    s = 2
    x_start = device.width - ((w + s) * (signal_range - 1) - 1)
    for link in range(0, signal_range):
      for _ in range(3):
        with canvas(device) as draw:
            print("Testing ramka...")
            time.sleep(1)
            for i in range(0, link):
                x0 = x_start + (w + s)*i
                y0 = y_start
                x1 = x_start + w + (s + w)*i
                y1 = h * i + 1
                draw.rectangle((x0, y0, x1, y1), fill="white")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

