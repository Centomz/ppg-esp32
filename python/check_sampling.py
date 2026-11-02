import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("data/ppg_raw.csv", delimiter=",", skiprows=1)
t = (data[:, 0] - data[0, 0]) / 1000.0     # seconds
ir = data[:, 2]

start = np.argmax(ir > 20000)              # first sample with the finger on
keep = t >= t[start] + 3                   # skip 3 s while the signal settles
t, ir = t[keep], ir[keep]

dt = np.diff(t) * 1000                     # time between two samples, in ms
print(f"mean dt = {dt.mean():.1f} ms, min = {dt.min():.0f} ms, max = {dt.max():.0f} ms")
print(f"mean rate = {1000 / dt.mean():.1f} Hz")

seg = t < t[0] + 10                        # first 10 s of clean signal
fig, axes = plt.subplots(2, 1, figsize=(10, 7))
axes[0].hist(dt, bins=50)
axes[0].set_xlabel("time between two samples (ms)")
axes[1].plot(t[seg], ir[seg])
axes[1].set_xlabel("time (s)")
axes[1].set_ylabel("IR (raw)")
plt.tight_layout()
plt.show()