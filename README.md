# 🖱️ Advanced Auto-Clicker
An advanced, high-speed autoclicker with a modern graphical user interface (GUI) and a built-in settings management system. 
This tool allows you to automate mouse clicks with extreme precision, making it ideal for gaming (such as Minecraft PvP) or testing purposes.

---

## 📸 Screenshots
<img width="517" height="450" alt="photo_2026-08-12_15-19-19" src="https://github.com/user-attachments/assets/5e53d04c-5c52-4d6e-8f0b-eb3f54dff181" />
<img width="523" height="453" alt="photo_2026-08-12_15-19-13" src="https://github.com/user-attachments/assets/fd5c8d7d-1313-4aec-9fd5-4d3d74847a10" />


## ✨ Features

* **Flexible Interval Settings:** Set click delays in minutes, seconds, or milliseconds.
* **Smart Randomization:** Built-in "Random Offset" feature to simulate human clicking and bypass anti-cheat systems.
* **Custom Hotkeys:** Easily bind any key (including Function keys like F1-F12) to start/stop the clicker.
* **Persistent Settings:** Your configuration is automatically saved to a `settings.json` file and loaded on startup.
* **Mouse Button Selection:** Choose between Left, Right, or Middle mouse buttons via a dropdown menu.
* **High Performance:** Uses Windows Multimedia API (`winmm.dll`) to achieve stable millisecond sleep accuracy.

---

## Technical tricks

* using WinApi function from ctypes for setting a time quantum:
  winmm = ctypes.windll.winmm
  winmm.timeBeginPeriod(1)
  winmm.timeEndPeriod(1)

