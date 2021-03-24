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

def moonlight():
    print('Starting Moonlight')
    print('Killing running moonlight-qt processes...')
    try:        
        check_call(['killall', 'moonlight-qt']) # this will error if none running so will avoid sleep below
        #os.system("killall moonlight-qt")
        sleep(2) # wait a bit for it to close propery (not sure if needed)
    except:
        print('Moonlight not running')

    system("QT_QPA_EGLFS_ALWAYS_SET_MODE=1 moonlight-qt &") # this way it run in background
    print("Done")

def moonlight_embedded():
    print('Starting Moonlight embedded')
    print('Killing running moonlight embedded processes')
    try:        
        check_call(['killall', 'moonlight']) # this will error if none running so will avoid sleep below
        #os.system("killall moonlight-qt")
        sleep(2) # wait a bit for it to close propery (not sure if needed)
    except:
        print('Moonlight not running')

    system("moonlight stream -1080 -bitrate 50000 -remote -quitappafter -app Steam &") # this way it run in background
    print("Done")


def shutdown():
    print("Shutting Down")
    led.on() #led will turn off after shutdown so know its happened
    sleep(1)
    check_call(['sudo', 'poweroff'])
    #system('shutdown now -h')

moonlight_btn = Button(14, hold_time=2)
moonlight_btn.when_held = moonlight_embedded

shutdown_btn = Button(15, hold_time=2)
shutdown_btn.when_held = shutdown

print("Starting Button Listener")
pause()

