#! /usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process
from display import Display
from rotary_encoder_right import RotaryEncoderRight

def main():
    runInParallel(start_encoders, start_display)

def start_encoders():
    encoder_right = RotaryEncoderRight()
    encoder_right.start()

def start_display():
    display = Display()
    display.start()

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
