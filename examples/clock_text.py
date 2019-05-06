#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

class ClockText():

    def __init__(self):
        self.refresh_info()


    def refresh_info(self):
        self.time_now = self.get_time()
        self.text_data = self.get_text_data()
        self.short_format = self.get_short_format()
        self.date_text = self.get_date_text()


    def get_text_data(self):
        return self.time_now.strftime("%d %B %Y  %A  %H:%M ")


    def get_short_format(self):
        if int(self.time_now.strftime("%S")) % 2 == 0:
            text = unicode(self.time_now.strftime("%H:%M"), 'utf-8')
        else:
            text = unicode(self.time_now.strftime("%H.%M"), 'utf-8')
        return text


    def get_time(self):
        return datetime.datetime.now()


    def get_date_text(self):
        return unicode(self.time_now.strftime("%d %B %Y  %A"), 'utf-8')
