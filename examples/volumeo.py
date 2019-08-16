#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
# pip install requests


class Volumeo():
    def __init__(self):
        self.volume_idle = 100
        self.volumeo_info = self.get_volumeo_info()
        self.volume_level = self.get_volume_level()
        self.status = self.get_status()
        self.tick_in_idle = self.volume_idle
        self.volume_level = self.get_volume_level()
        self.old_volume_level = self.get_volume_level()
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
        self.volume_level = self.get_volume_level()
        self.display = self.display_type()

    def get_volumeo_info(self):
        try:
            req = requests.get(url = "http://localhost:3000/api/v1/getstate", params =  {'address':'xxx'})
            vol_status = req.json()
        except requests.exceptions.RequestException as e:
            print 'exeption volumio req'
            print e
            vol_status = {}
        return vol_status

    def display_type(self):
        pleer_status = self.status
        if pleer_status in ['play', 'stop', 'pause']:
            if self.volume_level != self.old_volume_level:
                self.old_volume_level = self.volume_level
                self.tick_in_idle = 0
                display = 'volume'
            elif self.tick_in_idle < self.volume_idle:
                self.tick_in_idle += 1
                display = 'volume'
            else:
                display = 'main'
        else:
            display = 'undefined'
        return display

    def get_volume_level(self):
        info = self.volumeo_info
        return (info.get("volume", '0'))

    def time_elapsed(self):
        info = self.volumeo_info
        return (int(info.get("seek", 0))/1000)

    def time_total(self):
        info = self.volumeo_info
        return (int(info.get("duration", 0)))

    def get_uri_text(self):
        info = self.volumeo_info
        return (info.get("uri", '-'))

    def get_status(self):
        info = self.volumeo_info
        return info.get("status", '')

    def get_m_title(self):
        info = self.volumeo_info
        return info.get("title", '-')

    def artist(self):
        info = self.volumeo_info
        return info.get("artist", '-')

    def track_type(self):
        info = self.volumeo_info
        return info.get("trackType", '')

    def bitrate(self):
        info = self.volumeo_info
        return info.get("samplerate", '')

    def bitdepth(self):
        info = self.volumeo_info
        return info.get("bitdepth", '')

    def stream(self):
        info = self.volumeo_info
        return info.get("stream", '')

    def random_play(self):
        info = self.volumeo_info
        return info.get("random", '')

    def repeat_play(self):
        info = self.volumeo_info
        return info.get("repeat", '')

    def repeat_one(self):
        info = self.volumeo_info
        return info.get("repeatSingle", '')

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
        artist_name_data = self.artist().encode("utf-8")
        artist_name  = (artist_name_data[:31] + '..') if len(artist_name_data) > 33 else artist_name_data
        return "{:35s}  {}/{}/{}".format(artist_name, self.bitrate(), self.bitdepth(), self.track_type())

    def get_total_time(self):
        total = self.time_total()
        return self.secs_to_time(total)

    def get_elapsed_time(self):
        elapsed = self.time_elapsed()
        return self.secs_to_time(elapsed)

    def get_completed_proc(self):
        if self.time_total() > 0:
            return (self.time_elapsed() * 100) / self.time_total()
        else:
            return 0

    def get_title_uri(self):
        return "{} {}".format(self.get_m_title().encode("utf-8"), self.get_uri_text().encode("utf-8"))

