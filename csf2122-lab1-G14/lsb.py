import sys, wave
from bitstring import *

def decompose(data):
    return list(map(lambda x: 1 if x else 0, list(BitArray(bytes=data))))

audio = wave.open("chant1.wav")
sample_width = audio.getsampwidth()
sample_bits = sample_width * 8
print(f"Frames: {audio.getnframes()}")
frames = audio.readframes(audio.getnframes())
frames = [frames[i:i+sample_width] for i in range(0, len(frames), sample_width)]

n_lsb = 2
payload = []

for frame in frames:
    frame_bits = decompose(frame)
    bits = []
    for j in range(n_lsb):
        bits.append(frame_bits[sample_bits-n_lsb+j])

    payload += bits

# %  P  D
# 25 50 44
# 00100101 01010000 01000100

bit_string_to_find = "001001010101000001000100"

payload_string = "".join(str(bit) for bit in payload)
index = payload_string.index(bit_string_to_find)

print(index)
payload = payload[index:]

payload_lenght = len(payload)
if payload_lenght%8 != 0:
    payload = payload[:-(payload_lenght%8)]

byte_array = BitArray(payload).bytes

result = open("result.bin", "wb")
result.write(byte_array)
