import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

data = np.loadtxt("data/ppg_raw_exercice.csv", delimiter=",", skiprows=1)
t = (data[:, 0] - data[0, 0]) / 1000.0
ir = data[:, 2]

start = np.argmax(ir > 20000)          # first sample with the finger on
keep = t >= t[start] + 3               # skip 3 s while the signal settles
t, ir = t[keep], ir[keep]

fs = 1.0 / np.mean(np.diff(t))         # real sampling rate in Hz
print(f"fs = {fs:.1f} Hz")

low, high = 0.5, 5.0                   # band to keep, in Hz
b, a = butter(2, [low, high], btype="bandpass", fs=fs)
ir_f = filtfilt(b, a, ir)

fig, axes = plt.subplots(2, 1, sharex=True, figsize=(10, 7))
axes[0].plot(t, ir)
axes[0].set_ylabel("raw IR")
axes[1].plot(t, ir_f)
axes[1].set_ylabel("filtered IR")
axes[1].set_xlabel("time (s)")
plt.tight_layout()
plt.show()