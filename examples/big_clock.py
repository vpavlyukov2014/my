#! /usr/bin/env python
# -*- coding: utf-8 -*-

from demo_opts import get_device
from luma.core.render import canvas
from clock_text import ClockText
from PIL import ImageFont
import time
import os



def main():
    device = get_device()
    clock = ClockText()
    font1 = make_font("FreePixel.ttf", 16)
    font2 = make_font("FreePixel.ttf", 10)

    try:
        while True:
            with canvas(device) as draw:
                draw.text((0, 10), clock.date_text, fill="white", font=font1)
                draw.text((10, 10), clock.short_format, fill="white", font=font2)
                time.sleep(1)

    except KeyboardInterrupt:
        pass


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
