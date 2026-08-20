# 🖱️ Advanced Auto-Clicker
An advanced, high-performance auto-clicker specifically optimized for competitive gaming (like Minecraft Bedwars/PvP) and productivity tasks. 
Featuring a dual-hotkey profile system, this tool allows you to switch click modes instantly without leaving your game.

---

## 📸 Screenshots
<img width="520" height="454" alt="image" src="https://github.com/user-attachments/assets/4cc78820-5196-4f88-91bf-cfb42aecff31" />
<img width="521" height="451" alt="image" src="https://github.com/user-attachments/assets/537e84ff-06bf-45db-8a8f-313b838dd62b" />

## ✨ Features

* **🔥 Dual-Hotkey Profile System:** Configure two completely independent click actions simultaneously.
* **Flexible Interval Settings:** Configure click delays precisely using minutes, seconds, or milliseconds.
* **Smart Randomization:** Built-in "Random Offset" feature dynamically alters click intervals to mimic human behavior and bypass basic anti-cheat algorithms.
* **Language-Independent Hotkeys:** Re-engineered key hooking system utilizes hardware Virtual-Key (VK) codes, preventing hotkeys from breaking when switching keyboard layouts.
* **Persistent Settings:** Your complex multi-key configurations automatically save to `settings.json` and load seamlessly on startup.
* **High Performance Core:** Leverages Windows Multimedia API (`winmm.dll`) to achieve hardware-level millisecond sleep stability.

---

## 🚀 How to Install and Run

### Option 1: Quick Install (For Users)
1. Navigate to the **Releases** section on the right side of this repository.
2. Download the latest `AutoClicker_setup.exe`.
3. Run the installer and launch the app securely from your desktop shortcut (Installs outside restricted `Program Files` to prevent Windows Hook blocking).

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
