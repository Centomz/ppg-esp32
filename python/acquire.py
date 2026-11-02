import csv
import time
import serial                # pyserial: talks to the USB port
import numpy as np
import matplotlib.pyplot as plt

PORT = "/dev/cu.usbserial-0001"   # same port as in the Arduino IDE
BAUD = 115200                     # must match Serial.begin() in the sketch
DURATION_S = 30                   # how long we record
OUT = "ppg_raw.csv"

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)                     # the ESP32 reboots when the port opens
ser.reset_input_buffer()          # throw away old data

rows = []
start = time.time()
while time.time() - start < DURATION_S:
    line = ser.readline().decode(errors="ignore").strip()
    parts = line.split(",")
    if len(parts) != 3:
        continue                  # skip incomplete lines
    try:
        t_ms, red, ir = (int(p) for p in parts)
    except ValueError:
        continue                  # skip garbled lines
    rows.append((t_ms, red, ir))
ser.close()

with open(OUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["t_ms", "red", "ir"])
    writer.writerows(rows)

data = np.array(rows)
t = (data[:, 0] - data[0, 0]) / 1000.0     # seconds since the start
fs = len(t) / t[-1]                        # real sampling rate, in Hz
print(f"{len(t)} samples, real sampling rate = {fs:.1f} Hz")

plt.plot(t, data[:, 2])
plt.xlabel("time (s)")
plt.ylabel("IR (raw)")
plt.show()