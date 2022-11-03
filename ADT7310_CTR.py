#!/usr/bin/python3
# coding: utf-8
import spidev
import time


class ADT7310_CTR:
    def __init__(self, spi_port, device, max_hz=100000):
        self.port = spi_port
        self.device = device
        self.max_hz = max_hz
        self.initialize()

    def initialize(self):
        # create spi object
        self.spi = spidev.SpiDev()

        # open spi port, device
        self.spi.open(self.port, self.device)

        # reset register data
        self.clear_register()

        # set frequency
        self.spi.max_speed_hz = self.max_hz
        
        # Set mode
        self.spi.mode = 3

        self.enable_16bit_mode()
        self.enable_c_read_mode()

    def enable_16bit_mode(self):
        self.spi.xfer2([0x0C, 0x80])
        time.sleep(0.1)

    def clear_register(self):
        self.spi.xfer2([0xFF, 0xFF, 0xFF, 0xFF])
        time.sleep(0.005)

    def enable_c_read_mode(self):
        self.spi.xfer2([0x54])
        time.sleep(0.240)

    def disable_c_read_mode(self):
        self.spi.xfer2([0x50])

    def terminate(self):
        self.disable_c_read_mode()
        self.spi.close()

    def reinitialize(self):
        self.terminate()
        self.initialize()

    def temp(self):
        # return is [8bit, 8bit] of temp
        upper, lower = self.spi.xfer2([0x00, 0x00])

        # convert from [8bit,8bit] to 16bit
        temp = ((upper << 8) | lower)

        # is this negative?
        if temp & 0x8000:
            temp = temp - 65536

        # convert to celsius
        temp /= 128.0

        # If value is NULL, failed.
        if temp == 0:
            raise RuntimeError('Failed to get value')

        return temp
