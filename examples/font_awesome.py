#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

from __future__ import unicode_literals

"""
A wander through some (all, if you are patient) of the font awesome
TTF glyphs.

See: http://fontawesome.io/license/ for license details of included
fontawesome-webfont.ttf file
"""

import os
import sys
import random
from PIL import ImageFont

from demo_opts import get_device
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator

codes = [
    "\uf6ac"
]


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def infinite_shuffle(arr):
    copy = list(arr)
    while True:
        random.shuffle(copy)
        for elem in copy:
            yield elem


def main(num_iterations=sys.maxsize):
    device = get_device()
    regulator = framerate_regulator(fps=1)
    font = make_font("fa-regular-400.ttf", 10)

    for code in infinite_shuffle(codes):
        with regulator:
            num_iterations -= 1
            if num_iterations == 0:
                break

            with canvas(device) as draw:
                w, h = draw.textsize(text=code, font=font)
                left = (device.width - w) / 2
                top = (device.height - h) / 2
                draw.text((left, top), text=code, font=font, fill="white")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
