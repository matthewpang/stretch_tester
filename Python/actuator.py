__author__ = 'matthewpang'

import serial
import time
import pickle
import struct

serStepper = serial.Serial('/dev/cu.usbmodem14231', 230400)

def output_encoder(value):
    """
    Takes a 16 bit integer value, packs it little endian, then encapsulates it in the defined format
    [0xAA,LSByte,MSByte,OxFF]
    """

    b = struct.pack('<H', value)
    output = bytearray(4)
    output[0] = 0xAA
    output[1] = b[0]
    output[2] = b[1]
    output[3] = 0xFF

    return output

def output_decoder(array):
    """
    Takes a little endian byte array of format [0xAA,LSByte,MSByte,OxFF]
    and returns the corresponding 16 bit integer value
    """

    if len(array) != 4: #If the packet length is correct, otherwise return None
        return None

    if (array[0] == 0xAA) and (array[3] == 0XFF) and (len(array) == 4): #Check that the packet has the correct start and end frame
        a = array[2] << 8 | array[1]
        return int(a)



def serial_send(value):
    """
    Accepts a 16 bit unsigned int , encodes it and sends it, returns the bytearray that was sent
    """
    serStepper.reset_input_buffer()
    serStepper.reset_output_buffer()
    frame = output_encoder(value)
    serStepper.write(frame)
    return frame

def serial_receive():
    """
    Waits up to 5 seconds for a response after being called, decodes the byte array and returns a 16 bit unsigned int
    """
    timeout = time.time() + 5
    while (serStepper.in_waiting <= 3) and (time.time() < timeout): # Wait until correct number of packets, timeout if waiting too long
        time.sleep(0.001)
    else:
        serial_read = bytearray((serStepper.read(serStepper.in_waiting)))
        val = output_decoder(serial_read)
    return val

def arrival_wait():
    """
    Waits the get the arrival confirmation message 0xFF00 .
    Clears the buffers for cleanliness
    Waits up to 5 minutes for a response
    """
    timeout = time.time() + 300
    while (serial_receive() != 0xFF00) and (time.time() <= timeout):
        time.sleep(0.0001)
    serStepper.reset_input_buffer()
    serStepper.reset_output_buffer()

def go(pos=0):
    """
    Accepts a position and sends it serially.
    Waits for arrival confirmation
    """

    serial_send(pos)
    arrival_wait()


def gobetween(mode, min_position=0, max_position=0, zero_stretch_delay=0, max_stretch_delay=0):
    """
    Checks for the correct mode and positions , otherwise do nothing
    Goes to initial displacement, waits time, goes to maximum displacement, waits time, returns.
    """
    if (on_off == 0) or (mode != 0) or (min_position == max_position):
        return
    go(min_position)
    time.sleep(zero_stretch_delay)
    go(max_position)
    time.sleep(max_stretch_delay)
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
    """
    Does nasty nasty file I/O with nasty nasty global variables. I'm really sorry.
    """
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
    """
    Its obvious what this does.
    """
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
                #print("Running")
                gobetween(mode, int(initial_displacement), int(initial_displacement + stretch_length), zero_stretch_delay, max_stretch_delay)

if __name__ == '__main__':
    main()
