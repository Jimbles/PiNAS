#!/usr/bin/env/python3

# Script for shutdown and moonlight buttons.
# Add to rc.local for startup
# https://core-electronics.com.au/tutorials/how-to-make-a-safe-shutdown-button-for-raspberry-pi.html



from gpiozero import Button, LED
from subprocess import check_call
from signal import pause
from time import sleep
from os import system 

led = LED(18)

def shutdown():
    print("Shutting Down")
    led.on() #led will turn off after shutdown so know its happened
    sleep(1)
    check_call(['sudo', 'poweroff'])
    #system('shutdown now -h')

shutdown_btn = Button(15, hold_time=2)
shutdown_btn.when_held = shutdown

print("Starting Shutdown Button Listener")
pause()

