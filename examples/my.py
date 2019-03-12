#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

from demo_opts import get_device
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
import sys
import subprocess
import re
import math


def main():
    completed = 30
    device = get_device()
    for _ in range(200):
        with canvas(device) as draw:
            wifi_siganl(device, draw)
            clock(device, draw)
            progress_bar(device, draw, completed)
            time.sleep(1)


def clock(device, draw):
    left_padding = 0
    now = datetime.datetime.now()
    today_time = now.strftime("%d %B %Y  %A  %H:%M:%S ")
    text(draw, (left_padding, 0 ), today_time, fill="white", font=proportional(LCD_FONT) )


def progress_bar(device, draw, completed):
    h2 = 1
    w2 = 2
    color1 = "red"
    color2 = 'white'
    y_pad = 20
    display_w = device.width
    h = 12

    d1_x1 = 0
    d1_y1 = y_pad
    d1_x2 = (display_w * completed)/100 - w2
    d1_y2 = y_pad + h

    d2_x1 = d1_x2
    d2_y1 = d1_y1 - h2
    d2_x2 = d1_x2 + w2
    d2_y2 = d1_y2 + h2

    d3_x1 = d2_x2
    d3_y1 = d1_y1
    d3_x2 = display_w - 1
    d3_y2 = d1_y2

    draw.rectangle((d1_x1, d1_y1, d1_x2, d1_y2), fill=color1)
    draw.rectangle((d3_x1, d3_y1, d3_x2, d3_y2), outline=color1, fill="black")
    draw.rectangle((d2_x1, d2_y1, d2_x2, d2_y2), fill=color2)



def wifi_siganl(device, draw):
    wifi_info = get_wifi_info()
    wifi_level = wifi_info[0]
    wifi_desc = "{}/{}G".format(wifi_info[1], wifi_info[2])
    y_start = 0
    h = 2
    w = 2
    s = 2
    signal_range = 5
    x_start = device.width - ((w + s) * (signal_range) - 1)
    desc_width = len(wifi_desc) * 6
    desc_x_start = x_start - (desc_width + 5)
    text(draw, (desc_x_start, 0), wifi_desc, fill="white", font=proportional(LCD_FONT) )
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


def get_wifi_info():
    interface = "wlan0"
    proc = subprocess.Popen(["iwlist", interface, "scan"],stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()
    freq = re.search('(?<=Frequency:)(\d)', out).group(0)
    net_name = re.search('(?<=ESSID:")(.+)(")', out).group(1)
    result = re.search('(?<=Signal level=-)(\d+)', out).group(0)
    result_val = int(result)
    if math.isnan(result_val):
        level = 0
    else:
        level = result_val
    level_norm = wifi_level_desc(level)
    return [level_norm, net_name, freq]


def wifi_level_desc(level):
   if level == 0:
       return 0
   elif level <= 70:
       return 5
   elif 70 > level < 80:
       return 4
   elif 80 >= level < 90:
       return 3
   elif 90 >= level < 100:
       return 2
   elif 100 >= level < 110:
       return 1
   else:
       return 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
