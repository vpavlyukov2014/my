#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
sys.setdefaultencoding('utf8')
# pip install requests


class Volumeo():
    def __init__(self):
        self.refresh_info()

    def refresh_info(self):
        self.volumeo_info = self.get_volumeo_info()
        self.track_info = self.get_track_info()
        self.m_title = self.get_m_title()
        self.total_time = self.get_total_time()
        self.elapsed_time = self.get_elapsed_time()
        self.status = self.get_status()
        self.completed_procents = self.get_completed_proc()
        self.title_uri = self.get_title_uri()

    def get_volumeo_info(self):
        req = requests.get(url = "http://localhost:3000/api/v1/getstate", params =  {'address':'xxx'})
        return req.json()

    def time_elapsed(self):
        info = self.volumeo_info
        return (int(info["seek"])/1000)

    def time_total(self):
        info = self.volumeo_info
        return (int(info["duration"]))

    def get_uri_text(self):
        info = self.volumeo_info
        return (info["uri"])

    def get_status(self):
        info = self.volumeo_info
        return info["status"]

    def get_m_title(self):
        info = self.volumeo_info
        return info["title"]

    def artist(self):
        info = self.volumeo_info
        return info["artist"]

    def track_type(self):
        info = self.volumeo_info
        return info["trackType"]

    def bitrate(self):
        info = self.volumeo_info
        return info["samplerate"]

    def bitdepth(self):
        info = self.volumeo_info
        return info["bitdepth"]

    def stream(self):
        info = self.volumeo_info
        return info["stream"]

    def random_play(self):
        info = self.volumeo_info
        return info["random"]

    def repeat_play(self):
        info = self.volumeo_info
        return info["repeat"]

    def repeat_one(self):
        info = self.volumeo_info
        return info["repeatSingle"]

    def secs_to_time(self, secs):
      hours = secs / 3600
      secs = secs % 3600
      mins = secs / 60
      secs = secs % 60
      if (hours > 99):
         hours = 99
      time_text = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
      return time_text

    def get_track_info(self):
        artist_name_data = self.artist()
        artist_name  = (artist_name_data[:31] + '..') if len(artist_name_data) > 33 else artist_name_data
        return "{:35s}  {}/{}/{}".format(artist_name, self.bitrate(), self.bitdepth(), self.track_type())

    def get_total_time(self):
        total = self.time_total()
        return self.secs_to_time(total)

    def get_elapsed_time(self):
        elapsed = self.time_elapsed()
        return self.secs_to_time(elapsed)

    def get_completed_proc(self):
        return  ((self.time_elapsed() * 100) / self.time_total())

    def get_title_uri(self):
        return "{} {}".format(self.get_m_title(), self.get_uri_text())

