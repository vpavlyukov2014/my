#! /usr/bin/env python
# -*- coding: utf-8 -*-

from display import Display

def main():
    display = Display()
    display.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
