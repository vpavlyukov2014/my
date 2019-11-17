#! /usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
from rotary_encoder_right import RotaryEncoderRight
from rotary_encoder_left import RotaryEncoderLeft

def main():

    encoder_right = RotaryEncoderRight()
    encoder_left = RotaryEncoderLeft()
    print 'Start'
    print 'encoder on'
    encoder_right.start()
    encoder_left.start()
    try:
        while True:
            sleep(0.01)
    finally:
        encoder_left.stop()
        encoder_right.stop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
