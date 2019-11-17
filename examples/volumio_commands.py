#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests

class VolumeoCommands():
    def __init__(self):
        self.volume_idle = 100

    def send_volumeo_command(self, command):
        url = "http://localhost:3000/api/v1/commands/?cmd={}".format(command)
        print url
        try:
            req = requests.get(url = url, params =  {'address':'xxx'})
            vol_status = req.json()
        except requests.exceptions.RequestException as e:
            print 'exeption volumio req'
            print e
            vol_status = {}
        # print vol_status

    def vol_plus(self):
        command = 'volume&volume=plus'
        self.send_volumeo_command(command)

    def vol_minus(self):
        command = 'volume&volume=minus'
        self.send_volumeo_command(command)

    def toggle_play(self):
        command = 'toggle'
        self.send_volumeo_command(command)

    def toggle_next(self):
        command = 'next'
        self.send_volumeo_command(command)

    def toggle_prev(self):
        command = 'prev'
        self.send_volumeo_command(command)
