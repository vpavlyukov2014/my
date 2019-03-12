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
            # show_text_message(device, draw)
            time.sleep(1)


def clock(device, draw):
    left_padding = 10
    now = datetime.datetime.now()
    today_time = now.strftime("%d %B %Y  %A  %H:%M:%S ")
    text(draw, (left_padding, 0 ), today_time, fill="white", font=proportional(LCD_FONT) )


def show_text_message(device, draw):
    msg = 'sdfsdfsfdsdfssdfsdfsdf sdfsdfs dfs df sdf sd fs df sdf sd fs dfsdfsdfsdf'
    # device, msg, y_offset=0, fill=None, font=None,scroll_delay=0.03
    # show_message(device, msg, y_offset=30, fill="white", font=prop_font, scroll_delay=0.03)
    # show_message(device, msg, y_offset=20, fill="white", font=proportional(LCD_FONT), scroll_delay=1)
    for left_padding in range(30):
        text(draw, (left_padding, 20 ), msg, fill="white", font=proportional(LCD_FONT) )
        time.sleep(1)



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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
