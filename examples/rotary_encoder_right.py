#! /usr/bin/env python
# -*- coding: utf-8 -*-

from RPi import GPIO
from time import sleep


class RotaryEncoderRight():

    def __init__(self):

        self.clk = 20
        self.dt = 26
        self.sw = 13

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.counter = 0
        self.clkLastState = GPIO.input(self.clk)

    def start(self):
        try:
            while True:
                clkState = GPIO.input(self.clk)
                dtState = GPIO.input(self.dt)
                if clkState != self.clkLastState:
                    if dtState != clkState:
                            self.counter += 1
                    else:
                            self.counter -= 1
                    print self.counter
                self.clkLastState = clkState
                sleep(0.01)
        finally:
                GPIO.cleanup()
