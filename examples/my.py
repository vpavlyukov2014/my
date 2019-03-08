import time
import datetime

from demo_opts import get_device
from luma.core.render import canvas

def main():
    x_start = 0
    y_start = 0
    char_ht = 100
    device = get_device()
    for link in range(0, 4):
      for _ in range(10):
        with canvas(device) as draw:
            print("Testing ramka...")
            draw.rectangle(device.bounding_box, outline="white")
            time.sleep(3)
            for i in range(0, 4):
                ht = 2*i + 1
                x_off = 3*i + 1
                if link >= (i+1):
                    draw.rectangle(((x_start + x_off), (y_start + char_ht - (1+ht)), 2, ht), fill="white")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

