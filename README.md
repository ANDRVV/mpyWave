# What is mpyWave?

mpyWave is an opensource library that serves to send bits and receive them from a pin for RF, fully compatible with all hardwares.
![Waves](https://raw.githubusercontent.com/ANDRVV/mpyWave/main/26855362.jpg)

# Examples
```python
import mpyWave

wave = mpyWave.Wave(UARTid = 0, rxPin = 17, txPin = 16)

wave.sendWave("0")
wave.sendWave("1")

wave.sendWaves("011100010101110100001010111010000101000")

wave.overflow("1") # It sends waves compulsively

print(mpyWave.getValidBits(wave.recvWaves(length = 40)))
```
