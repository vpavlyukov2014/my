#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re
import math


class Wifi():


    def __init__(self):
        self.refresh()

    def get_info_text(self):
        return "{}/{}G".format(self.info[1], self.info[2])

    def get_info(self):
        # print("Refresh wifi info")
        interface = "wlan0"
        proc = subprocess.Popen(["iwlist", interface, "scanning last"], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        out, err = proc.communicate()
        freq = self.search_reg('(?<=Frequency:)(\d)', out, 0)
        net_name = self.search_reg('(?<=ESSID:")(.+)(")', out, 1)
        result = self.search_reg('(?<=Signal level=-)(\d+)', out, 0)
        result_val = int(result)
        if math.isnan(result_val):
            level = 0
        else:
            level = result_val
        level_norm = self.wifi_level_desc(level)
        return [level_norm, net_name, freq]

    def refresh(self):
        self.info = self.get_info()
        self.info_text = self.get_info_text()

    def search_reg(self, patrn, str, group_num):
        try:
            result = re.search(patrn, str).group(group_num)
        except:
            result = '0'
        return result


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
