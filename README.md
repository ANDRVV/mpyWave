# What is mpyWave?

mpyWave is an opensource library that serves to send bits and receive them from a pin, fully compatible with all hardwares.
It is especially recommended if the hardware is a radio wave transmitter or receiver.
![Waves](https://raw.githubusercontent.com/ANDRVV/mpyWave/main/26855362.jpg)

# Examples
```python
import mpyWave

wave = mpyWave.Wave(protocol = 1, pin = 16)

wave.sendWave("0")
wave.sendWave("1")

wave.sendWaves("011100010101110100001010111010000101000")

wave.overflow("1") # It sends waves compulsively

print(recvWaves(length = 8))
```
