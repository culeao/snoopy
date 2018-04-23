from machine import Pin
import network
import time
def led_state():
    p2 = Pin(2, Pin.OUT)
    p2.value(0)
    time.sleep_ms(500)
    p2.value(1)
    time.sleep_ms(500)
    p2.value(0)
    time.sleep_ms(500)
    p2.value(1)
    time.sleep_ms(500)
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    p2 = Pin(2, Pin.OUT)
    sta_if.active(False)
    if not sta_if.isconnected():
        p2.value(0)
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('wifi_name', 'wifi_secret')
        while not sta_if.isconnected():
            pass
    if sta_if.isconnected():
        print('connect success')
        led_state()
        print('network config:', sta_if.ifconfig())
do_connect()
