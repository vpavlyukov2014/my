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
                w = device.width
                w1, h1 = draw.textsize(clock.date_text, font1)
                w2, h2 = draw.textsize(clock.short_format, font2)

                x1 = (w - w1)/2
                y1 = 0
                y2 = h1 - 5
                x2 = (w - w2)/2

                draw.text((x1, y1), clock.date_text, fill="white", font=font1)
                draw.text((x2, y2), clock.short_format, fill="white", font=font2)
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
