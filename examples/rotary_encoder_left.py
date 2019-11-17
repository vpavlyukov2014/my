#! /usr/bin/env python
# -*- coding: utf-8 -*-

from RPi import GPIO
from volumio_commands import VolumeoCommands

class RotaryEncoderLeft:

    def __init__(self):
        self.clk = 22
        self.dt = 27
        self.sw = 17

        self.vol_commands = VolumeoCommands()
        self.lastDirection = -1
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.clk, GPIO.IN)
        GPIO.setup(self.dt, GPIO.IN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start(self):
        GPIO.add_event_detect(self.clk, GPIO.FALLING, callback=self._clockCallback, bouncetime=250)
        GPIO.add_event_detect(self.sw, GPIO.FALLING, callback=self._switchCallback, bouncetime=300)

    def stop(self):
        GPIO.remove_event_detect(self.clk)
        GPIO.remove_event_detect(self.sw)
        GPIO.cleanup()

    def _clockCallback(self, pin):
        if GPIO.input(self.clk) == 0:
            data = GPIO.input(self.dt)
            if data != self.lastDirection:
                self.lastDirection = data
            elif data == 1:
                self.vol_commands.toggle_prev()
            else:
                self.vol_commands.toggle_next()

    def _switchCallback(self, pin):
        if GPIO.input(self.sw) == 0:
            self.vol_commands.toggle_play()
