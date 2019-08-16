#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time

from power_relay import PowerRelay

def main():
    power_relay = PowerRelay()
    print 'Start'
    time.sleep(10)

    print 'relay on'
    power_relay.power_on()
    time.sleep(10)

    print 'relay off'
    power_relay.power_off()
    time.sleep(10)

    print 'relay on'
    power_relay.power_on()
    time.sleep(10)

    print 'relay on'
    power_relay.power_on()
    time.sleep(10)

    print 'relay off'
    power_relay.power_off()
    time.sleep(10)

    print 'relay off'
    power_relay.power_off()
    time.sleep(10)

    print 'relay on'
    power_relay.power_on()
    time.sleep(10)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
