from machine import Pin
import time

BIT_00 = str(0x0)
BIT_01 = str(0x1)

NO_TIMEOUT = 0x6e6f74696d65
DELAY_OPERATOR = 0xf4240

SYNC_HIGH = 1
SYNC_LOW = 31

PULSE_HIGH_BIT00 = 1
PULSE_LOW_BIT00 = 3
PULSE_HIGH_BIT01 = 3
PULSE_LOW_BIT01 = 1

TX = 0x1d36
RX = 0x1c6e

PROTOCOL_01 = [350, 1, 31, 1, 3, 3, 1]
PROTOCOL_02 = [650, 1, 10, 1, 2, 2, 1]
PROTOCOL_03 = [100, 30, 71, 4, 11, 9, 6]
PROTOCOL_04 = [380, 1, 6, 1, 3, 3, 1]
PROTOCOL_05 = [500, 6, 14, 1, 2, 2, 1]
PROTOCOL_06 = [200, 1, 10, 1, 5, 1, 1]

PROTOCOLS = [None, PROTOCOL_01, PROTOCOL_02, PROTOCOL_03, PROTOCOL_04, PROTOCOL_05, PROTOCOL_06]

class Wave():
    def __init__(self, protocol : int, pin : int):
        self.pin = Pin(pin, Pin.OUT)
        self.intPin = pin
        self.pinMode = TX
        self.protocol = PROTOCOLS[protocol]

    def sendWave(self, Bit : str):
        if self.pinMode == RX:
            self.pin = Pin(self.intPin, Pin.OUT)
            self.pinMode = TX
            self.syncTx()
        if str(Bit) == BIT_00:
            HighPulse = PULSE_HIGH_BIT00 * self.protocol[0]
            LowPulse = PULSE_LOW_BIT00 * self.protocol[0]
        elif str(Bit) == BIT_01:
            HighPulse = PULSE_HIGH_BIT01 * self.protocol[0]
            LowPulse = PULSE_LOW_BIT01 * self.protocol[0]
        else:
            raise Exception("Wrong bit!")
        self.pin.high()
        self.setDelay(HighPulse / DELAY_OPERATOR)
        self.pin.low()
        self.setDelay(LowPulse / DELAY_OPERATOR)

    def sendWaves(self, Bits : str):
        if self.pinMode == RX:
            self.pin = Pin(self.intPin, Pin.OUT)
            self.pinMode = TX
            self.syncTx()
        for Bit in str(Bits):
            if Bit == BIT_00:
                HighPulse = PULSE_HIGH_BIT00 * self.protocol[0]
                LowPulse = PULSE_LOW_BIT00 * self.protocol[0]
            elif Bit == BIT_01:
                HighPulse = PULSE_HIGH_BIT01 * self.protocol[0]
                LowPulse = PULSE_LOW_BIT01 * self.protocol[0]
            else:
                raise Exception("Wrong bit!")
            self.pin.high()
            self.setDelay(HighPulse / DELAY_OPERATOR)
            self.pin.low()
            self.setDelay(LowPulse / DELAY_OPERATOR)
    
    def recvWaves(self, length : int = 24):
        if self.pinMode == TX:
            self.pin = Pin(self.intPin, Pin.IN, Pin.PULL_DOWN)
            self.pinMode = RX
        bits = ""
        while True:
            if len(bits) >= 24:
                return bits
            else:
                try:
                    if self.pin.value() != 1:
                        raise Exception()
                    self.setDelay(PULSE_HIGH_BIT00 * self.protocol[0] / DELAY_OPERATOR)
                    if self.pin.low() != 0:
                        raise Exception()
                    self.setDelay(PULSE_LOW_BIT00 * self.protocol[0] / DELAY_OPERATOR)
                    bits += "0"
                except:
                    try:
                        if self.pin.value() != 1:
                            raise Exception()
                        self.setDelay(PULSE_HIGH_BIT01 * self.protocol[0] / DELAY_OPERATOR)
                        if self.pin.low() != 0:
                            raise Exception()
                        self.setDelay(PULSE_LOW_BIT01 * self.protocol[0] / DELAY_OPERATOR)
                        bits += "1"
                    except:
                        continue

    def overflow(self, timeout : int = NO_TIMEOUT, Bit : int = 1):
        if self.pinMode == RX:
            self.pin = Pin(self.intPin, Pin.OUT)
            self.pinMode = TX
            self.syncTx()
        if timeout == NO_TIMEOUT:
            while True:
                self.sendWave(Bit)
        else:
            beforeTime = time.time()
            while True:
                self.sendWave(Bit)
                currentTime = time.time()
                if (currentTime - beforeTime) > timeout:
                    break

    def syncTx(self):
        if self.pinMode == RX:
            self.pin = Pin(self.intPin, Pin.OUT)
            self.pinMode = TX
        self.pin.high()
        self.setDelay((SYNC_HIGH * self.protocol[0]) / DELAY_OPERATOR)
        self.pin.low()
        self.setDelay((SYNC_LOW * self.protocol[0]) / DELAY_OPERATOR)

    def setDelay(self, delay):
        end = time.time() + delay - (delay / 100)
        while time.time() < end:
            time.sleep(delay / 100)
    
