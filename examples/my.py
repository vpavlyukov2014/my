import time
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
                draw.rectangle(x_start + x_off, y_start + char_ht - (1+ht), 2, ht, fill="white")
        time.sleep(5)
        draw.text((device.width - 10, 30 + 16), 'World!', fill="purple")



