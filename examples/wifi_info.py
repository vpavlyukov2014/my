#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import math


class Wifi():


    def __init__(self):
        self.refresh()


    def info(self):
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
        level_norm = self.wifi_level_desc(level)
        return [level_norm, net_name, freq]


    def refresh(self):
        print("Refresh wifi info")
        return


    def wifi_level_desc(self, level):
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
