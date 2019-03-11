#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import datetime
import locale
from PIL import ImageFont
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

from demo_opts import get_device
from luma.core.render import canvas
from luma.core.legacy import show_message
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT


def main():
    wifi_level = 2
    device = get_device()
    for _ in range(200):
        wifi_level = random.randint(0, 5)
        with canvas(device) as draw:
            wifi_siganl(device, draw, wifi_level)
            clock(device, draw)
            # show_text_message(device)
            time.sleep(1)


def clock(device, draw):
    left_padding = 10
    now = datetime.datetime.now()
    today_time = now.strftime("%d %B %Y, %A  %H:%M:%S ")
    # draw.text((left_padding, 0), today_time, font=font(12), fill="white")
    # text(draw, xy, txt, fill=None, font=None)
    text(draw, (left_padding, 0 ), today_time, fill="white", font=proportional(LCD_FONT) )


def show_text_message(device):
    msg = 'sdfsdfsfdsdfssdfsdfsdf sdfsdfs dfs df sdf sd fs df sdf sd fs dfsdfsdfsdf'
    # device, msg, y_offset=0, fill=None, font=None,scroll_delay=0.03
    # show_message(device, msg, y_offset=30, fill="white", font=prop_font, scroll_delay=0.03)
    show_message(device, msg, y_offset=20, fill="white", font=proportional(LCD_FONT))


# def prop_font():
    # return proportional(LCD_FONT)


def font(size):
    return make_font('Impact.ttf', size)


# def encode_text(text):
    # return text.decode('cp1251')
     # return unicode(text, 'utf-8')


def wifi_siganl(device, draw, wifi_level):
    y_start = 0
    h = 2
    w = 2
    s = 2
    signal_range = 5
    x_start = device.width - ((w + s) * (signal_range) - 1)
    for i in range(0, signal_range):
        if i < wifi_level:
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


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

