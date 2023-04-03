from machine import Pin, UART
import time

BIT_00 = str(0x0)
BIT_01 = str(0x1)

NO_TIMEOUT = 0x6e6f74696d65

TX = 0x1d36
RX = 0x1c6e

HEX_CHARS = "1234567890abcdef"

class Wave():
    def __init__(self, UARTid : int,  rxPin : int, txPin : int, baudrate : int = 9600):
        self.pin = UART(UARTid, tx = Pin(txPin), rx = Pin(rxPin), baudrate = baudrate, bits = 8, parity = None, stop = 2)

    def sendWave(self, bit : str):
        if str(bit) == "0":
            self._send0x0()
        elif str(bit) == "1":
            self._send0x1()
        else:
            raise Exception("Wrong bit!")

    def sendWaves(self, bits : str):
        for Bit in str(bits):
            if str(Bit) == "0":
                self._send0x0()
            elif str(Bit) == "1":
                self._send0x1()
            else:
                raise Exception("Wrong bit!")
    
    def recvWaves(self, length : int = 0):
        while True:
            if self.pin.any():
                if length == 0:
                    response = self.pin.read()
                else:
                    response = self.pin.read(length)
                if response == None:
                    pass
                else:
                    return getBinaryFromHexBytes(response)

    def overflow(self, timeout : int = NO_TIMEOUT, Bit : str = "1"):
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

    def _send0x0(self):
        self.pin.write(BIT_00)

    def _send0x1(self):
        self.pin.write(BIT_01)

def getBinaryFromHexBytes(hexbytes : bytes):
    formatted = str(hexbytes)[2:-1].replace("\\x", "").replace(" ", "")
    newFormatted = ""
    for hbyte in formatted:
        if hbyte in HEX_CHARS:   
            newFormatted += hbyte
    try:
        return bin(int(newFormatted, 16))[2:]
    except:
        return None

def getValidBits(bits : str, chunksize : int = 8, counter : int = 3):
        if bits == None:
            return None
        maxCount = counter - 1
        maxEscape = round(maxCount / 2)
        chunks = []
        for i in range(1, len(bits), chunksize):
            chunks.append(bits[i:i + chunksize])
        if len(chunks) < 1:
            return None
        finalstring = ""
        for chunk in chunks:
            if len(chunk) < (maxCount * 2):
                finalstring += chunk
                continue
            escape = 0
            counter = 1
            charwork = ""
            valid = True 
            for char in chunk:
                if str(chunk).index(char) == 0:
                    charwork = char
                    continue
                if charwork == char:
                    counter += 1
                else:
                    if counter >= maxCount:
                        escape += 1
                    charwork = char
                    counter = 1
                if escape >= maxEscape:
                    valid = False
            if valid:
                finalstring += chunk
        if finalstring == "":
            return None
        return finalstring
