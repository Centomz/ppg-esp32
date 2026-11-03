# Build journal

---

## 2026-10-29: first contact with the ESP32

**Goal:** check that the board, the cable and the toolchain work before adding the sensor.

**Done**
- Plugged the ESP32 to the Mac (USB-C). Nothing visible happens: the board shows up as a serial port (`/dev/cu.usbserial-0001`), not as a drive.
- Installed the *esp32* board package (Espressif Systems) in the Arduino IDE. Selected *ESP32 Dev Module*.
- Uploaded the Blink example.

**Problems and fixes**
- "Missing FQBN": no board definition installed yet. Fixed by installing the *esp32* package from the Boards Manager (not "Arduino ESP32 Boards", which is only for the Arduino Nano ESP32).
- Compilation error `expected ';' before 'pinMode'`: a stray `'g'` typed in the code. Fixed by deleting it.

---

## 2026-10-29: wiring the MAX30102

**Goal:** connect the sensor and detect it on the I2C bus.

**Done**
- Wired VIN to 3V3, GND to GND, SDA to GPIO 21, SCL to GPIO 22 on a breadboard.
- Uploaded an I2C scanner sketch.

**Problems and fixes**
- The sensor had no pins, so contact was unreliable. The scanner reported "No I2C device found" unless I pressed the module on loose pins.

**What I learned:**
- I2C connects chips with two wires: SDA (data) and SCL (clock). Each device has an address, and a scanner sketch finds it (`0x57` for the MAX30102).
- Wire with the power off, and use 3.3 V only.
- A part pressed onto loose pins is not a reliable electrical contact: I2C worked only while I held the sensor.

---

## 2026-10-30: soldering and first real data

**Goal:** make the connection reliable and read raw red/IR values.

**Done**
- First soldering of my life: 4 straight header pins (VIN, SDA, SCL, GND) on the sensor, held straight by the breadboard.
- The scanner now finds the device at address `0x57`.
- Uploaded the SparkFun MAX3010x example to read red and IR values.

**Problems and fixes**
- Garbled characters in the Serial Monitor: the baud rate in the code and in the monitor did not match. Fixed by using `Serial.begin(115200)` / 115200 baud.
- Serial Plotter showed no visible pulse: the plot contained three curves (millis, red, IR) on one scale. Fixed by selecting only the IR value.

**What I learned:**
- Soldering a header: hold the strip straight in a breadboard, solder one end pin, check the alignment, then solder the others. After soldering, the scanner found `0x57` every time.
- The baud rate must be the same in the code and in the Serial Monitor, otherwise the text is garbled.
- The Serial Plotter draws every number on the line on one scale. A pulse of about 80 counts is invisible next to a timestamp of 500,000, so I plotted only the IR value.

---

## 2026-10-31 to 2026-11-02: Python pipeline

**Goal:** turn the raw signal into a heart rate, understanding each step.

**Done**
- Created the project folder, a virtual environment and a Git repository.
- Stage 1: `acquire.py` records 30 s to CSV. Real sampling rate measured: about 99 Hz.
- Stage 2: `check_sampling.py` shows regular spacing of about 10 ms between samples.
- Stage 3: `filter_ppg.py` applies a 0.5 to 5 Hz Butterworth band-pass filter with `filtfilt`. The drift disappears and one wave per heartbeat remains.
- Stage 4: `heart_rate.py` detects peaks and computes the heart rate.

**Problems and fixes**
- With a prominence threshold of 0.3 times the standard deviation, small bumps after each beat were counted as beats (instantaneous rates of 126 and 149 bpm at rest). Raising the threshold to 0.9 fixed it.

**Results (preliminary)**
- Rest: 60.4 bpm vs 60 bpm (smartwatch).
- After 20 squats: 83.4 bpm vs 80 bpm (smartwatch).

**What I learned:**
- The raw signal has a large constant part (DC, light through skin, tissue and bone) and a tiny pulsing part (AC, blood volume changing with each beat), about 0.15% of the total here. The work is to remove the DC and the drift and keep the AC.
- With this sensor, more blood means more light absorbed, so the raw value goes down at each beat.
- Filter cutoffs are in Hz, so the filter needs the real sampling rate, which I measure from the timestamps (about 99 Hz) instead of assuming 100 Hz.
- A band-pass filter (0.5 to 5 Hz) keeps 30 to 300 beats per minute, and removes slow drift and fast noise. `filtfilt` runs it forward and backward so the beats are not shifted in time.
- `find_peaks`: `distance` sets the minimum time between peaks (0.4 s means at most 150 bpm), and `prominence` sets how much a peak must stand out. Too low a prominence counted the small bump after each beat (dicrotic notch) as a beat, giving impossible rates (126 and 149 bpm at rest).
- Always check results against physiology (a resting heart rate cannot jump from 60 to 149 bpm in one beat) and against an independent reference. I tuned the threshold on the same recording I judged it on, so I need more recordings.

---

## Next

- Stronger validation (more recordings, Bland-Altman).
- SpO2 from the red/IR signals.
- Real-time display.
