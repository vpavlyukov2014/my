#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Scrolling artist + song and play/pause indicator
"""

import os
import time
from PIL import ImageFont, Image, ImageDraw
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.image_composition import ImageComposition, ComposableImage
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT


titles = [
    ("Bridge over troubled water wdfwef wefwef wef wefwef wef wef", "Simon & Garfunkelw wefwe fw efwe fwe fw efwefwe")
]


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



# ------- main


device = get_device()



image_composition = ImageComposition(device)

try:
    while True:
        for title in titles:
            synchroniser = Synchroniser()
            ci_song = ComposableImage(TextImage(device, title[0]).image, position=(0, 1))
            ci_artist = ComposableImage(TextImage(device, title[1]).image, position=(0, 30))
            song = Scroller(image_composition, ci_song, 100, synchroniser)
            artist = Scroller(image_composition, ci_artist, 100, synchroniser)
            cycles = 0

            while cycles < 3:
                artist.tick()
                song.tick()
                time.sleep(0.025)
                cycles = song.get_cycles()

                with canvas(device, background=image_composition()) as draw:
                    image_composition.refresh()
                    draw.rectangle(device.bounding_box, outline="white")

            del artist
            del song

except KeyboardInterrupt:
    pass
