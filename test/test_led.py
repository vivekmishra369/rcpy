import pytest

import time
import rcpy.gpio as gpio
import rcpy.led as led

def test1():

    led.green.on()
    assert led.green.is_on()
    assert gpio.Input(led.green.pin).is_low()
    
    led.green.off()
    assert led.green.is_off()
    assert gpio.Input(led.green.pin).is_low()
    
    led.red.on()
    assert led.red.is_on()
    assert gpio.Input(led.red.pin).is_low()
    
    led.red.off()
    assert led.red.is_off()
    assert gpio.Input(led.red.pin).is_low()

if __name__ == '__main__':

    test1()
