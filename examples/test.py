#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time

from rotary_encoder_right import RotaryEncoderRight

def main():
    encoder = RotaryEncoderRight()
    print 'Start'
    time.sleep(10)

    print 'relay off'
    encoder.start()
    time.sleep(10)

    print 'encoder off'

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
