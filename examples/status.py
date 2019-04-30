#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Status():

    def __init__(self, volumeo):
        self.tick_in_idle = 0
        self.volumeo = volumeo
        self.show_player = True


    def tick(self):
        if self.volumeo.status == 'play':
            self.tick_in_idle = 0
        else:
            self.tick_in_idle += 1
        self.set_status()


    def set_status(self):
        if self.tick_in_idle > 30:
            self.show_player = False
        else:
            self.show_player = True
