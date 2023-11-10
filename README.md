<h1 align="center">What is mpyWave?</h1>

<p align="center">mpyWave is an opensource library that serves to send bits and receive them from a pin for RF, fully compatible with all hardwares.</p>

<h3 align="center">Examples</h3>

<div align="center" style="display:grid;place-items:center;">
  
```python
import mpyWave

wave = mpyWave.Wave(protocol = 1, pin = 16)

wave.sendWave("0")
wave.sendWave("1")

wave.sendWaves("011100010101110100001010111010000101000")

wave.overflow("1") # It sends waves compulsively

print(mpyWave.getValidBits(wave.recvWaves(length = 40)))
```
</div>
