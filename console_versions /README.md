# C++ Blazing Fast Autoclicker Version

## Technical Features

### 1. Package Click Sending (Burst Mode)
By default, Windows has a thread quantum limitation of ~15.6 ms. We bypassed this restriction using the `timeBeginPeriod(1);` and `timeEndPeriod(1);` commands. Furthermore, if you set the delay to less than 10 ms, the program automatically switches to a **Burst Mode**. It packages multiple clicks together and executes them while maintaining a stable 10 ms sleep interval to keep CPU usage at 0%. 
This optimization allows the clicker to achieve a maximum of **~670-700 CPS** (with `CLICK_DELAY = 0.001` or a 1 ms interval).

### 2. Build Peculiarities
1. This code relies heavily on the native Windows API (WinAPI).
2. If you are using the Microsoft MSVC compiler, the required library is linked automatically via `#pragma comment(lib, "winmm.lib")` included in the source code.
3. For MinGW or Clang compilers, you must manually pass the **`-lwinmm`** flag at the very end of your build command. For example:
```bash
g++ main.cpp -o clicker.exe -lwinmm
clang++ main.cpp -o clicker.exe -lwinmm
```

## First Iteration Clicker Function (Legacy)
This was the baseline implementation. Due to Windows thread context-switching overhead, this function caps out at a maximum of **~480-500 CPS** (with `CLICK_DELAY = 0.001` or a 1 ms interval).

```cpp
void clicker() {
    using namespace Mouse;

    while(!exit_program) {
        if (clicking) {
            if (selected_button == Button::Left) {
                ClickLeft();
            }
            else if (selected_button == Button::Right) {
                ClickRight();
            }

            DWORD sleep = CLICK_DELAY * 1000.0;
            this_thread::sleep_for(chrono::milliseconds(sleep));

            // Alternative methods tested for performance:
            // this_thread::sleep_for(chrono::duration<double>(CLICK_DELAY));
            // DWORD ms_sleep = (DWORD)(CLICK_DELAY * 1000.0);
            // Sleep(ms_sleep);
        }
        else {
            Sleep(100);
        }
    }
}
```

## In plans
Anti-cheat bypass for Minecraft pvp servers to avoid being banned due to the same click interval
