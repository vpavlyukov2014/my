#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
from PIL import ImageFont

from volumeo import Volumeo
from wifi_info import Wifi
from clock_text import ClockText
from status import Status
from power_relay import PowerRelay

class Display():

    def __init__(self):
        print 'Start display'
        self.volumeo = Volumeo()
        self.wifi = Wifi()
        self.clock_text = ClockText()
        self.power_relay = PowerRelay()
        self.clock_font1 = self.make_font("arialbi.ttf", 14)
        self.clock_font2 = self.make_font("ariali.ttf", 60)
        self.clock_font3 = self.make_font("ariali.ttf", 40)
        self.device = get_device()
        self.clock_w = self.device.width
        self.d_h = (self.device.height - 10)
        self.display_status = Status(self.volumeo)
        self.i = 0
        self.beg_val = 0

    def start(self):
        print 'Start display start'
        try:
            while True:
                print 'while true'
                if self.volumeo.display == 'undefined':
                    self.show_loading()
                elif self.display_status.show_player:
                    self.power_on()
                    self.show_player()
                else:
                    self.power_off()
                    self.show_clock()
        except KeyboardInterrupt:
            pass

    def show_player(self):
        with canvas(self.device) as draw:
            self.wifi_siganl(self.device, draw, self.wifi)
            self.clock(draw, self.clock_text)
            text(draw, (0, self.d_h), self.volumeo.title_uri, fill="white", font=proportional(LCD_FONT) )
            if self.volumeo.display == 'main':
                self.track_info(draw, self.volumeo)
                self.progress_bar(self.device, draw, self.volumeo)
                self.music_timer(self.device, draw, self.volumeo)
                self.draw_status_sym(self.device, draw, self.volumeo)
                time.sleep(1)
            elif self.volumeo.display == 'volume':
                self.volume_bar(draw, self.volumeo)
                time.sleep(0.025)
        self.volumeo.refresh_info()
        self.wifi.refresh()
        self.clock_text.refresh_info()
        self.display_status.tick()

    def show_clock(self):
         with canvas(self.device) as draw:
            self.clock_text.refresh_info()
            self.volumeo.refresh_info()
            clock_w1, clock_h1 = draw.textsize(self.clock_text.date_text, self.clock_font1)
            clock_w2, clock_h2 = draw.textsize(self.clock_text.short_format, self.clock_font2)
            clock_x1 = (self.clock_w - clock_w1)/2
            clock_y1 = 0
            clock_y2 = clock_h1 - 8
            clock_x2 = (self.clock_w - clock_w2)/2
            draw.text((clock_x1, clock_y1), self.clock_text.date_text, fill="white", font=self.clock_font1)
            draw.text((clock_x2, clock_y2), self.clock_text.short_format, fill="white", font=self.clock_font2)
            self.display_status.tick()
            time.sleep(1)

    def power_on(self):
        self.power_relay.power_on()

    def power_off(self):
        self.power_relay.power_off()

    def track_info(self, draw, volumeo):
        h = 12
        left_padding = 0
        text(draw, (left_padding, h ), volumeo.track_info, fill="white", font=proportional(LCD_FONT))

    def show_loading(self):
        with canvas(self.device) as draw:
            self.volumeo.refresh_info()
            loading_message = "Loading {}".format(self.router_val())
            draw.text((10, 10), loading_message, fill="white", font=self.clock_font3)
        time.sleep(0.5)


    def volume_bar(self, draw, volumeo):
        volumeo.refresh_info()
        volume_text = "Volume: {}".format(volumeo.volume_level)
        draw.text((25, 10), volume_text, fill="white", font=self.clock_font3)


    def music_timer(self, device, draw, volumeo):
        h = 32
        left_padding = 0
        text(draw, (left_padding, h ), volumeo.elapsed_time, fill="white", font=proportional(LCD_FONT) )
        x_start = device.width - left_padding - len(volumeo.total_time) * 6 + 6
        text(draw, (x_start, h ), volumeo.total_time, fill="white", font=proportional(LCD_FONT) )


    def draw_status_sym(self, device, draw, volumeo):
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


    def clock(self, draw, clock_text):
        left_padding = 0
        text(draw, (left_padding, 0 ), clock_text.text_data, fill="white", font=proportional(LCD_FONT) )


    def progress_bar(self, device, draw, volumeo):
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

    def wifi_siganl(self, device, draw, wifi):
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

    def make_font(self, name, size):
        font_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'fonts', name))
        return ImageFont.truetype(font_path, size)


    def router_val(self):
        begs = ['>', '->', '-->', '--->', '---->', '---<', '--<', '-<', '<']
        if self.beg_val < 8:
            res = begs[self.beg_val]
            self.beg_val += 1
        else:
            self.beg_val = 0
            res = begs[self.beg_val]
        return res


