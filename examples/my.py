#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
from luma.core.image_composition import ImageComposition, ComposableImage
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT

from scroll import TextImage
from scroll import Synchroniser
from scroll import Scroller
from volumeo import Volumeo
from wifi_info import Wifi
from clock_text import ClockText

def main():
    volumeo = Volumeo()
    wifi = Wifi()
    clock_text = ClockText()

    device = get_device()
    d_h = (device.height - 10)
    image_composition = ImageComposition(device)
    i = 0

    try:
        while True:
            if (i == 10):
                print("refresh{}".format(i))
                i = 0
                volumeo.refresh_info()
                wifi.refresh()
                clock_text.refresh_info()
            else:
                i += 1

            synchroniser = Synchroniser()
            ci_song = ComposableImage(TextImage(device, volumeo.title_uri).image, position=(0, d_h))
            song = Scroller(image_composition, ci_song, 75, synchroniser)
            cycles = 0

            while cycles < 3:
                song.tick()
                time.sleep(0.025)
                cycles = song.get_cycles()

                with canvas(device, background=image_composition()) as draw:
                    image_composition.refresh()
                    wifi_siganl(device, draw, wifi)
                    clock(draw, clock_text)
                    track_info(draw, volumeo)
                    progress_bar(device, draw, volumeo)
                    music_timer(device, draw, volumeo)
                    draw_status_sym(device, draw, volumeo)

            del song

    except KeyboardInterrupt:
        pass


def track_info(draw, volumeo):
    h = 12
    left_padding = 0
    text(draw, (left_padding, h ), volumeo.track_info, fill="white", font=proportional(LCD_FONT) )


def music_timer(device, draw, volumeo):
    h = 32
    left_padding = 0
    text(draw, (left_padding, h ), volumeo.elapsed_time, fill="white", font=proportional(LCD_FONT) )
    x_start = device.width - left_padding - len(volumeo.total_time) * 6 + 6
    text(draw, (x_start, h ), volumeo.total_time, fill="white", font=proportional(LCD_FONT) )


def draw_status_sym(device, draw, volumeo):
    color = 'white'
    h = 32
    wx = 3
    zh = 14
    started_x = device.width/2 - 3*wx
    started_y = h + zh + 2
    status_val = volumeo.status
    if status_val == 'play':
        d1_x1 = started_x
        d1_y1 = started_y
        d1_x3 = started_x
        d1_y3 = started_y - zh
        d1_x2 = started_x + wx*3
        d1_y2 = started_y - zh/2
        draw.polygon([(d1_x1, d1_y1), (d1_x2, d1_y2), (d1_x3, d1_y3)], fill=color)
    elif status_val == 'stop':
        d1_x1 = started_x
        d1_y1 = started_y
        d1_x2 = d1_x1 + zh
        d1_y2 = d1_y1 - zh
        draw.rectangle((d1_x1, d1_y1, d1_x2, d1_y2), outline=color, fill='red')
    elif status_val == 'pause':
        d1_x1 = started_x
        d1_y1 = started_y
        d1_x2 = d1_x1 + wx
        d1_y2 = d1_y1 - zh
        draw.rectangle((d1_x1, d1_y1, d1_x2, d1_y2), outline=color, fill="red")
        d2_x1 = d1_x1 + wx*2
        d2_y1 = d1_y1
        d2_x2 = d2_x1 + wx
        d2_y2 = d1_y2
        draw.rectangle((d2_x1, d2_y1, d2_x2, d2_y2), outline=color, fill="red")


def clock(draw, clock_text):
    left_padding = 0
    text(draw, (left_padding, 0 ), clock_text.text_data, fill="white", font=proportional(LCD_FONT) )


def progress_bar(device, draw, volumeo):
    h2 = 1
    w2 = 2
    color1 = "red"
    color2 = 'white'
    y_pad = 25
    display_w = device.width
    h = 4
    d1_x1 = 0
    d1_y1 = y_pad
    d1_x2 = (display_w * volumeo.completed_procents)/100 - w2
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


def wifi_siganl(device, draw, wifi):
    wifi_level =  wifi.info[0]
    wifi_desc = wifi.info_text
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
