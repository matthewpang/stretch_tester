__author__ = 'matthewpang'

import serial
import time
import pickle
import struct

serStepper = serial.Serial('/dev/cu.usbmodem14231', 230400)
time.sleep(3)

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

    if (array[0] == 0xAA) and (array[3] == 0XFF) and len(array) == 4: #Check that the packet has the correct start and end frame
        a = array[2] << 8 | array[1]
        return int(a)

def serial_send(value):
    """
    Accepts a 16 bit unsigned int , encodes it and sends it, returns the bytearray that was sent
    """
    frame = output_encoder(value)
    serStepper.write(frame)
    print(str(value))
    return frame

def serial_receive():
    """
    Waits up to 5 seconds for a response after being called, decodes the byte array and returns a 16 bit unsigned int
    """
    timeout = time.time() + 5
    while (serStepper.in_waiting <= 3) and (time.time() < timeout): # Wait until correct number of packets, timeout if waiting too long
        time.sleep(0.0001)
    else:
        serial_read = (serStepper.read(serStepper.in_waiting))
        val = output_decoder(serial_read)
        print(str(val))
    return val

def arrival_wait():
    """
    Waits the get the arrival confirmation message 0xFF00 .
    Clears the buffers for cleanliness
    """
    timeout = time.time() + 600
    while (serial_receive() != 0xFF00) and (time.time() <= timeout):
        time.sleep(0.0001)
    serStepper.reset_input_buffer()
    serStepper.reset_output_buffer()

def go(pos=0):
    """
    Accepts a position and sends it serially.
    Waits for arrival confirmation
    #Optionally times the difference between instruction and respose - uncomment.
    """

    sent = time.time()
    serial_send(pos)
    arrival_wait()
    received = time.time()
    print(str(received - sent))

go(0x0000)