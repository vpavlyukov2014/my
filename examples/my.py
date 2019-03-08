import time
import datetime

from demo_opts import get_device
from luma.core.render import canvas

def main():
    link = 5
    x_start = 10
    y_start = 10
    char_ht = 10
    device = get_device()
    with canvas(device) as draw:
        for i in range(0, 4):
            ht = 2*i + 1
            x_off = 3*i + 1
            if link >= (i+1):
                draw.rectangle(((x_start + x_off), (y_start + char_ht - (1+ht)), 2, ht), fill="white")
        time.sleep(5)
        # draw.text((device.width - 10, 30 + 16), 'World!', fill="purple")
        # time.sleep(20)
        # for x in range(40):
        #     with canvas(device) as draw:
        #         now = datetime.datetime.now()
        #         draw.text((x, 4), str(now.date()), fill="white")
        #         draw.text((10, 16), str(now.time()), fill="white")
        #         time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass


