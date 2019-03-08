import time
import datetime

from demo_opts import get_device
from luma.core.render import canvas

def main():
    x_start = 0
    y_start = 0
    char_ht = 10
    device = get_device()
    for link in range(0, 4):
      for _ in range(3):
        with canvas(device) as draw:
            print("Testing ramka...")
            time.sleep(1)
            draw.rectangle((0, 0, link, 10), fill="red")
            # for i in range(0, link):
            #     x_off = i*3
            #     draw.rectangle(((x_start + x_off), (y_start + char_ht - (1+ht)), 1, ht), fill="white")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

