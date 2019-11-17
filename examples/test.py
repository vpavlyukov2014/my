#! /usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
from rotary_encoder_right import RotaryEncoderRight

def main():

    encoder = RotaryEncoderRight()
    print 'Start'
    print 'encoder on'
    encoder.start()
    try:
        while True:
            sleep(0.01)
    finally:
        encoder.stop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
