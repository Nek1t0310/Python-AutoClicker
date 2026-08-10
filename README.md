# cpp-python-autoclicker
autoclicker on cpp and python, different implementations

simple autoclicker which might come in handy in minecraft pvp :)

you can also test this clicker in the Python UI click test!

## Technical tricks

* using WinApi function from ctypes for setting a time quantum:
  winmm = ctypes.windll.winmm
  winmm.timeBeginPeriod(1)
  winmm.timeEndPeriod(1)

