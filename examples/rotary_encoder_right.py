#! /usr/bin/env python
# -*- coding: utf-8 -*-

from RPi import GPIO
from time import sleep
from volumio_commands import VolumeoCommands

class RotaryEncoderRight:

    def __init__(self):
        self.clk = 20
        self.dt = 26
        self.sw = 13

        self.vol_commands = VolumeoCommands()
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.clk, GPIO.IN)
        GPIO.setup(self.dt, GPIO.IN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start(self):
        GPIO.add_event_detect(self.clockPin, GPIO.FALLING, callback=self._clockCallback, bouncetime=250)
        GPIO.add_event_detect(self.switchPin, GPIO.FALLING, callback=self._switchCallback, bouncetime=300)

    def stop(self):
        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.switchPin)
        GPIO.cleanup()

    def _clockCallback(self):
        if GPIO.input(self.clockPin) == 0:
            data = GPIO.input(self.dataPin)
            if data == 1:
                self.vol_commands.vol_minus()
            else:
                self.vol_commands.vol_plus()

    def _switchCallback(self):
        if GPIO.input(self.switchPin) == 0:
            self.switchCallback()
            self.vol_commands.toggle_play()
