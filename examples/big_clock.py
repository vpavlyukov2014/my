#! /usr/bin/env python
# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

import os
import time

from demo_opts import get_device
from luma.core.render import canvas
from clock_text import ClockText
from PIL import ImageFont


def main():
    device = get_device()
    clock = ClockText()
    font1 = make_font("Andale_Mono.ttf", 14)
    font2 = make_font("Andale_Mono.ttf", 58)

    try:
        while True:
            with canvas(device) as draw:
                draw.text((10, 0), unicode(clock.date_text, 'utf-8'), fill="white", font=font1)
                draw.text((30, 10), clock.short_format, fill="white", font=font2)
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
