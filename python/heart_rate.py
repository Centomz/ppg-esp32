import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

data = np.loadtxt("data/ppg_raw_exercice.csv", delimiter=",", skiprows=1)
t = (data[:, 0] - data[0, 0]) / 1000.0
ir = data[:, 2]

start = np.argmax(ir > 20000)
keep = t >= t[start] + 3
t, ir = t[keep], ir[keep]

fs = 1.0 / np.mean(np.diff(t))
b, a = butter(2, [0.5, 5.0], btype="bandpass", fs=fs)
sig = filtfilt(b, a, ir)

# ignore the first and last second (filter edge effects)
ok = (t > t[0] + 1) & (t < t[-1] - 1)
t, sig = t[ok], sig[ok]

peaks, _ = find_peaks(sig, distance=int(0.4 * fs), prominence=0.3 * np.std(sig))

ibi = np.diff(t[peaks])             # time between beats, in seconds
median_ibi = np.median(ibi)
good = (ibi > 0.6 * median_ibi) & (ibi < 1.4 * median_ibi)
hr = 60.0 / ibi                     # instantaneous heart rate, in bpm

print(f"{len(peaks)} beats detected")
print(f"mean HR = {60.0 / ibi.mean():.1f} bpm")
print(f"min / max instantaneous HR = {hr.min():.0f} / {hr.max():.0f} bpm")
print(f"{good.sum()} of {len(ibi)} intervals kept")
print(f"mean HR (cleaned) = {60.0 / ibi[good].mean():.1f} bpm")

fig, axes = plt.subplots(2, 1, sharex=True, figsize=(10, 7))
axes[0].plot(t, sig)
axes[0].plot(t[peaks], sig[peaks], "rx")
axes[0].set_ylabel("filtered IR")
axes[1].plot(t[peaks][1:], hr, "o-")
axes[1].set_ylabel("heart rate (bpm)")
axes[1].set_xlabel("time (s)")
plt.tight_layout()
plt.show()