#! /usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

class PowerRelay():

    def __init__(self):
        self.channel = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)

    def power_on(self):
        GPIO.output(self.channel, GPIO.HIGH)

    def power_off(self):
        GPIO.output(self.channel, GPIO.LOW)

