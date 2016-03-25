__author__ = 'matthewpang'

import serial
import time
import pickle

serStepper = serial.Serial('/dev/cu.usbmodem1421', 230400)


def go(pos=0):
    serStepper.flushOutput()
    serStepper.flushInput()
    #serStepper.write(chr(pos)) #Write the correctly formatted byte packets here


def gobetween(mode, min_position=0, max_position=0, zero_stretch_delay=0, max_stretch_delay=0):
    if (on_off == 0) or (mode != 0) or (min_position == max_position):
        return

    go(max_position)
    time.sleep(max_stretch_delay)
    go(min_position)
    time.sleep(zero_stretch_delay)

    return


#Define Global Variables - this is a dirty dirty hack

on_off = 0
v_zero = 0
stretch_length = 0
initial_displacement = 0
zero_stretch_delay = 0
max_stretch_delay = 0
go_max = 0
go_min = 0
go_zero = 0
mode = 0
reset = 0

def read():
    global on_off
    global v_zero
    global stretch_length
    global initial_displacement
    global zero_stretch_delay
    global max_stretch_delay
    global go_max
    global go_min
    global go_zero
    global mode
    global reset
    file = open('stream', 'r')
    a = pickle.load(file)

    #Array from UI - this is a dirty hack, I hate it ,but it works and I'm feeling lazy because TKinter is not thread safe.

    on_off = a[0]
    v_zero = a[1]
    stretch_length = a[2]
    initial_displacement = a[3]
    zero_stretch_delay = a[4]
    max_stretch_delay = a[5]
    go_max = a[6]
    go_min = a[7]
    go_zero = a[8]
    mode = a[9]
    reset = a[10]


def main():
    while True:
        try:
            read()
        except (IOError, EOFError):
            continue

        if go_min == 1:
            go(initial_displacement)

        elif go_max == 1:
            go(initial_displacement + stretch_length)

        elif go_zero == 1:
            go(0)

        elif reset == 1:
            go(65281) #0xFF01

        else:

            if (on_off == 1):
                # print("Running")
                gobetween(mode, int(initial_displacement), int(initial_displacement + stretch_length), zero_stretch_delay, max_stretch_delay)

if __name__ == '__main__':
    main()
