#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Volumeo():
    def __init__(self):
        self.refresh_info()

    def refresh_info(self):
        self.volumeo_info = self.get_volumeo_info()
        self.track_info = self.get_track_info()
        print("Refresh volumeo info")

    def get_volumeo_info(self):
        return {
            "status":"stop", #"play" "pause" "stop"
            "position":0,
            "title":"Привет заголовок песни очень длинный и предлинный как незнайчто",
            "artist":"Группа Браво",
            "album":"Мой альбом",
            "albumart":"/albumart?web=Baustelle/La%20malavita/extralarge&path=%2FNAS%2FMusic%2FBaustelle%20-%20La%20Malavita",
            "uri":"mnt/NAS/Music/Baustelle - La Malavita/02 la guerra è finita.mp3",
            "trackType":"mp3",
            "seek":42240,
            "duration":262,
            "samplerate":"44.1 KHz",
            "bitdepth":"24 bit",
            "channels":2,
            "random": None,
            "repeat": None,
            "repeatSingle": False,
            "consume": False,
            "volume":41,
            "mute": False,
            "stream":"mp3",
            "updatedb": False,
            "volatile": False,
            "service":"mpd"
        }

    def time_elapsed(self):
        info = self.volumeo_info
        return (int(info["seek"])/1000)


    def time_total(self):
        info = self.volumeo_info
        return (int(info["duration"]))


    def status(self):
        info = self.volumeo_info
        return info["status"]


    def m_title(self):
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

