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
from luma.core.virtual import viewport
from luma.core.sprite_system import framerate_regulator


def main():
    wifi_level = 2
    device = get_device()
    for _ in range(200):
        wifi_level = random.randint(0, 5)
        with canvas(device) as draw:
            wifi_siganl(device, draw, wifi_level)
            clock(device, draw)
            show_text_message(device)
            time.sleep(1)


def clock(device, draw):
    left_padding = 10
    now = datetime.datetime.now()
    today_time = now.strftime("%d %B %Y  %A  %H:%M:%S ")
    text(draw, (left_padding, 0 ), today_time, fill="white", font=proportional(LCD_FONT) )


def show_text_message(device):
    msg = 'sdfsdfsfdsdfssdfsdfsdf sdfsdfs dfs df sdf sd fs df sdf sd fs dfsdfsdfsdf'
    # device, msg, y_offset=0, fill=None, font=None,scroll_delay=0.03
    # show_message(device, msg, y_offset=30, fill="white", font=prop_font, scroll_delay=0.03)
    show_message(device, msg, y_offset=20, fill="white", font=proportional(LCD_FONT), scroll_delay=0.03)


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


def textsize(txt, font):
    """
    Calculates the bounding box of the text, as drawn in the specified font.
    This method is most useful for when the
    :py:class:`~luma.core.legacy.font.proportional` wrapper is used.

    :param txt: The text string to calculate the bounds for
    :type txt: str
    :param font: The font (from :py:mod:`luma.core.legacy.font`) to use.
    """
    src = [c for ascii_code in txt for c in font[ord(ascii_code)]]
    return (len(src), 8)


def show_message(device, msg, y_offset=0, fill=None, font=None,
                 scroll_delay=0.03):
    """
    Scrolls a message right-to-left across the devices display.

    :param device: The device to scroll across.
    :param msg: The text message to display (must be ASCII only).
    :type msg: str
    :param y_offset: The row to use to display the text.
    :type y_offset: int
    :param fill: The fill color to use (standard Pillow color name or RGB
        tuple).
    :param font: The font (from :py:mod:`luma.core.legacy.font`) to use.
    :param scroll_delay: The number of seconds to delay between scrolling.
    :type scroll_delay: float
    """
    fps = 0 if scroll_delay == 0 else 1.0 / scroll_delay
    regulator = framerate_regulator(fps)
    with canvas(device) as draw:
        w, h = textsize(msg, font)

    x = device.width
    virtual = viewport(device, width=w + x + x, height=10) #device.height)

    with canvas(virtual) as draw:
        text(draw, (x, y_offset), msg, font=font, fill=fill)

    i = 0
    while i <= w + x:
        with regulator:
            virtual.set_position((i, 0))
            i += 1


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

