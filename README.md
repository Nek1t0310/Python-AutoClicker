# 🖱️ Advanced Auto-Clicker
An advanced, high-speed autoclicker with a modern graphical user interface (GUI) and a built-in settings management system. 
This tool allows you to automate mouse clicks with extreme precision, making it ideal for gaming (such as Minecraft PvP) or testing purposes.

---

## 📸 Screenshots
<img width="523" height="453" alt="photo_2026-08-12_15-19-13" src="https://github.com/user-attachments/assets/fd5c8d7d-1313-4aec-9fd5-4d3d74847a10" />
<img width="517" height="450" alt="photo_2026-08-12_15-19-19" src="https://github.com/user-attachments/assets/5e53d04c-5c52-4d6e-8f0b-eb3f54dff181" />

## ✨ Features

* **Flexible Interval Settings:** Set click delays in minutes, seconds, or milliseconds.
* **Smart Randomization:** Built-in "Random Offset" feature to simulate human clicking and bypass anti-cheat systems.
* **Custom Hotkeys:** Easily bind any key (including Function keys like F1-F12) to start/stop the clicker.
* **Persistent Settings:** Your configuration is automatically saved to a `settings.json` file and loaded on startup.
* **Mouse Button Selection:** Choose between Left, Right, or Middle mouse buttons via a dropdown menu.
* **High Performance:** Uses Windows Multimedia API (`winmm.dll`) to achieve stable millisecond sleep accuracy.

---

## 🚀 How to Install and Run

### Option 1: Quick Install (For Users)
1. Download the **`AutoClicker_setup.exe`** file from the root of this repository.
2. Run the installer and follow the instructions on the screen.
3. Launch the app using the desktop shortcut.

### Option 2: Run from Source (For Developers)
If you want to modify the code or run it manually:

1. Clone the repository:
   ```bash
   git clone https://github.com/Nek1t0310/Python-AutoClicker
   ```
2. Install the required dependencies:
   ```bash
   pip install pynput
   ```
3. Run the application:
   ```bash
   python autoclicker/autoclicker_GUI.py
   ```

---

## 🛠️ Technical Details & Optimization
* **Language:** Python 3.9+ (GUI) / C++ (Console Core)
* **GUI Library:** Tkinter (Custom styled layouts)
* **Input Hooking:** `pynput` for non-blocking global hotkey detection.
* **Timer Precision:** Leverages `winmm.timeBeginPeriod(1)` to bypass the default 15.6ms Windows OS quantum restriction, forcing high-precision intervals.

---

## 📂 Repository Structure
* `autoclicker/` — Main GUI project source code, assets, and icons.
* `console_versions/` — Lightweight, console, minimalist implementations in Python and high-speed C++(Bonus).
