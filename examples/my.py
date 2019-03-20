#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import locale
import subprocess
import re
import math
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
from PIL import ImageFont, Image, ImageDraw
from luma.core.render import canvas
from luma.core.image_composition import ImageComposition, ComposableImage
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT



def main():
    device = get_device()
    image_composition = ImageComposition(device)

    try:
        while True:
            synchroniser = Synchroniser()
            ci_song = ComposableImage(TextImage(device, m_title()).image, position=((device.height - 10), 1))
            song = Scroller(image_composition, ci_song, 100, synchroniser)
            cycles = 0

            while cycles < 3:
                song.tick()
                time.sleep(0.025)
                cycles = song.get_cycles()

                with canvas(device, background=image_composition()) as draw:
                    image_composition.refresh()
                    draw.rectangle(device.bounding_box, outline="white")
                    wifi_siganl(device, draw)
                    clock(draw)
                    track_info(device, draw)
                    progress_bar(device, draw)
                    music_timer(device, draw)
                    draw_status_sym(device, draw)

            del song

    except KeyboardInterrupt:
        pass


def volumeo_info():
    info = {
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
    return info


def track_info(device, draw):
    h = 12
    left_padding = 0
    artist_name_data = artist()
    artist_name  = (artist_name_data[:31] + '..') if len(artist_name_data) > 33 else artist_name_data
    info_text = "{:35s}  {}/{}/{}".format(artist_name, bitrate(), bitdepth(), track_type())
    text(draw, (left_padding, h ), info_text, fill="white", font=proportional(LCD_FONT) )


def music_timer(device, draw):
    h = 32
    left_padding = 0
    total = time_total()
    elapsed = time_elapsed()
    total_text = secs_to_time(total)
    elapsed_text = secs_to_time(elapsed)
    info_text = elapsed_text
    text(draw, (left_padding, h ), info_text, fill="white", font=proportional(LCD_FONT) )
    x_start = device.width - left_padding - len(total_text) * 6 + 6
    text(draw, (x_start, h ), total_text, fill="white", font=proportional(LCD_FONT) )

def draw_status_sym(device, draw):
    i = 0
    color = 'white'
    if i % 2 == 0:
        flash_color = 'white'
    else:
        flash_color = 'red'
    h = 32
    wx = 3
    zh = 14
    started_x = device.width/2 - 3*wx
    started_y = h + zh + 2

    status_val = status()
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
        draw.rectangle((d1_x1, d1_y1, d1_x2, d1_y2), outline=flash_color, fill="red")
        d2_x1 = d1_x1 + wx*2
        d2_y1 = d1_y1
        d2_x2 = d2_x1 + wx
        d2_y2 = d1_y2
        draw.rectangle((d2_x1, d2_y1, d2_x2, d2_y2), outline=flash_color, fill="red")


def secs_to_time(secs):
  hours = secs / 3600
  secs = secs % 3600
  mins = secs / 60
  secs = secs % 60
  if (hours > 99):
     hours = 99
  time_text = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
  return time_text


def time_elapsed():
    info = volumeo_info()
    return (int(info["seek"])/1000)


def time_total():
    info = volumeo_info()
    return (int(info["duration"]))


def status():
    info = volumeo_info()
    return info["status"]


def m_title():
    info = volumeo_info()
    return info["title"]


def artist():
    info = volumeo_info()
    return info["artist"]


def track_type():
    info = volumeo_info()
    return info["trackType"]


def bitrate():
    info = volumeo_info()
    return info["samplerate"]


def bitdepth():
    info = volumeo_info()
    return info["bitdepth"]

def stream():
    info = volumeo_info()
    return info["stream"]


def random_play():
    info = volumeo_info()
    return info["random"]


def repeat_play():
    info = volumeo_info()
    return info["repeat"]


def repeat_one():
    info = volumeo_info()
    return info["repeatSingle"]


def clock(draw):
    left_padding = 0
    now = datetime.datetime.now()
    today_time = now.strftime("%d %B %Y  %A  %H:%M:%S ")
    text(draw, (left_padding, 0 ), today_time, fill="white", font=proportional(LCD_FONT) )


def progress_bar(device, draw):
    completed = (time_elapsed() * 100) / time_total()
    h2 = 1
    w2 = 2
    color1 = "red"
    color2 = 'white'
    y_pad = 25
    display_w = device.width
    h = 4

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


class TextImage():
    def __init__(self, device, dr_text):
        h = 8
        w = len(dr_text)*6
        self.image = Image.new(device.mode, (w, h))
        draw = ImageDraw.Draw(self.image)
        text(draw, (0, 0 ), dr_text, fill="white", font=proportional(LCD_FONT) )
        del draw
        self.width = w
        self.height = h


class Synchroniser():
    def __init__(self):
        self.synchronised = {}

    def busy(self, task):
        self.synchronised[id(task)] = False

    def ready(self, task):
        self.synchronised[id(task)] = True

    def is_synchronised(self):
        for task in self.synchronised.iteritems():
            if task[1] is False:
                return False
        return True


class Scroller():
    WAIT_SCROLL = 1
    SCROLLING = 2
    WAIT_REWIND = 3
    WAIT_SYNC = 4

    def __init__(self, image_composition, rendered_image, scroll_delay, synchroniser):
        self.image_composition = image_composition
        self.speed = 1
        self.image_x_pos = 0
        self.rendered_image = rendered_image
        self.image_composition.add_image(rendered_image)
        self.max_pos = rendered_image.width - image_composition().width
        self.delay = scroll_delay
        self.ticks = 0
        self.state = self.WAIT_SCROLL
        self.synchroniser = synchroniser
        self.render()
        self.synchroniser.busy(self)
        self.cycles = 0
        self.must_scroll = self.max_pos > 0

    def __del__(self):
        self.image_composition.remove_image(self.rendered_image)

    def tick(self):

        # Repeats the following sequence:
        #  wait - scroll - wait - rewind -> sync with other scrollers -> wait
        if self.state == self.WAIT_SCROLL:
            if not self.is_waiting():
                self.cycles += 1
                self.state = self.SCROLLING
                self.synchroniser.busy(self)

        elif self.state == self.WAIT_REWIND:
            if not self.is_waiting():
                self.synchroniser.ready(self)
                self.state = self.WAIT_SYNC

        elif self.state == self.WAIT_SYNC:
            if self.synchroniser.is_synchronised():
                if self.must_scroll:
                    self.image_x_pos = 0
                    self.render()
                self.state = self.WAIT_SCROLL

        elif self.state == self.SCROLLING:
            if self.image_x_pos < self.max_pos:
                if self.must_scroll:
                    self.render()
                    self.image_x_pos += self.speed
            else:
                self.state = self.WAIT_REWIND

    def render(self):
        self.rendered_image.offset = (self.image_x_pos, 0)

    def is_waiting(self):
        self.ticks += 1
        if self.ticks > self.delay:
            self.ticks = 0
            return False
        return True

    def get_cycles(self):
        return self.cycles



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
