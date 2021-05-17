import soundfile as sf
import numpy as np
from utils import signals_to_string

filepath = 'result.wav'
data, _ = sf.read(filepath)

print(len(data))
size = len(data)
data = set(["{:.6f}".format(d) for d in data])

rev_data = []

for i in range(size):
  k = np.sin(i * 439.97 / 44100 * (2 * np.pi))
  ks = "{:.6f}".format(k)
  if ks in data:
    rev_data.append(k)
  else:
    rev_data.append("x")


signal = []
for i in range(0, len(rev_data), 2000):
  if rev_data[i:i+2000].count("x") > 500:
    signal.append(0)
  else:
    signal.append(1)

print(len(rev_data))
print(signal)
print(signals_to_string(signal))
