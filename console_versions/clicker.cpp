#include <windows.h>
#include <iostream>
#include <mmsystem.h>
#include <thread>
// #include <chrono>
using namespace std;

// #pragma comment(lib, "winmm.lib") // <- для компилятора MSVC

namespace Mouse {
    enum class Button {
        Left,
        Right
    };

    void PressLeft() {
        INPUT in = {0};
        in.type = INPUT_MOUSE;
        in.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
        SendInput(1, &in, sizeof(INPUT));
    }

    void RealeseLeft() {
        INPUT in = {0};
        in.type = INPUT_MOUSE;
        in.mi.dwFlags = MOUSEEVENTF_LEFTUP;
        SendInput(1, &in, sizeof(INPUT));
    }

    void PressRight() {
        INPUT in = {0};
        in.type = INPUT_MOUSE;
        in.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN;
        SendInput(1, &in, sizeof(INPUT));
    }

    void RealeseRight() {
        INPUT in = {0};
        in.type = INPUT_MOUSE;
        in.mi.dwFlags = MOUSEEVENTF_RIGHTUP;
        SendInput(1, &in, sizeof(INPUT));
    }

    void ClickLeft() {
        PressLeft();
        RealeseLeft();
    }

    void ClickRight() {
        PressRight();
        RealeseRight();
    }
}

const int EXIT_KEY = VK_HOME;
const int ON_KEY = VK_OEM_PLUS;
const int OFF_KEY = VK_OEM_MINUS;

bool clicking = false;
bool exit_program = false;
double CLICK_DELAY = 0.1;

Mouse::Button selected_button = Mouse::Button::Left;

void clicker() {
    using namespace Mouse;

    const DWORD BASE_SLEEP_MS = 10;
    const double BASE_SLEEP_SEC = BASE_SLEEP_MS / 1000.0;

    while(!exit_program) {
        if (clicking) {
            if (CLICK_DELAY <= BASE_SLEEP_SEC) {

                int click_to_send = static_cast<int>(BASE_SLEEP_SEC / CLICK_DELAY);
                if (click_to_send < 1) {
                    click_to_send = 1;
                }

                for (int i = 0; i < click_to_send; i++) {
                    if (selected_button == Button::Left) {
                        ClickLeft();
                    }
                    else if (selected_button == Button::Right) {
                        ClickRight();
                    }
                }
                Sleep(BASE_SLEEP_MS);
            }
            else {
                if (selected_button == Button::Left) {
                    ClickLeft();
                }
                else if (selected_button == Button::Right) {
                    ClickRight();
                }

                // DWORD sleep = CLICK_DELAY * 1000.0;
                // this_thread::sleep_for(chrono::milliseconds(sleep));

                // this_thread::sleep_for(chrono::duration<double>(CLICK_DELAY));

                DWORD ms_sleep = (DWORD)(CLICK_DELAY * 1000.0);
                Sleep(ms_sleep);
            }
        }
        else {
            Sleep(100);
        }
    }
}

void on_press_keyboard() {
    bool last_on_state = false; 
    bool last_off_state = false;

    while (!exit_program) {
        bool current_on_pressed = (GetAsyncKeyState(ON_KEY) < 0);
        bool current_off_pressed = (GetAsyncKeyState(OFF_KEY) < 0);
        bool current_exit_pressed = (GetAsyncKeyState(EXIT_KEY) < 0);

        if (current_exit_pressed) {
            cout << "Программа завершена. " << "\n";
            clicking = false;
            exit_program = true;
            break;
        }

        if (current_on_pressed && !last_on_state) {
            if (!clicking) {
                clicking = true;
                cout << "Автокликер: Включен" << "\n";
            }
            else {
                clicking = false;
                cout << "Автокликер: Выключен (Пауза)" << "\n";
            }
        }

        if (current_off_pressed && !last_off_state) {
            clicking = false;
            cout << "Автокликер: Остановлен. Возврат к настройкам..." << "\n";
            break;
        }

        last_on_state = current_on_pressed;
        last_off_state = current_off_pressed;

        Sleep(20);
    }
}

void on_click_setup() {
    using namespace Mouse;

    cout << "Нажмите кнопку мыши (прям на жкране) для выбрра" << "\n";

    while (true) {
        if (GetAsyncKeyState(VK_LBUTTON) < 0) {
            selected_button = Button::Left;
            cout << "Выбрана левая кнопка мыши (ЛКМ)" << "\n";

            while (GetAsyncKeyState(VK_LBUTTON) & 0x8000) {
                Sleep(10);
            }

            break;
        }

        if (GetAsyncKeyState(VK_RBUTTON) < 0) {
            selected_button = Button::Right;
            cout << "Выбрана правая кнопка мыши (ПКМ)" << "\n";

            while (GetAsyncKeyState(VK_RBUTTON) & 0x8000) {
                Sleep(10);
            }

            break;
        }
        Sleep(10);
    }

}

int main() {
    timeBeginPeriod(1);
    thread click_thread(clicker);

    while (!exit_program) {
        cout << "===========================" << "\n";
        cout << "===Настройки Автокликера===" << "\n";
        cout << "===========================" << "\n";

        double user_input;

        while (true) {
            cout << "Введите задержку в секундах или 0 для выхода: " << "\n";
            cin >> user_input;

            if (cin.fail()) {
                cin.clear();
                cin.ignore(10000, '\n');
                cout << "Ошибка, введите число. Установлена задержка по умолчанию: 0.1 сек." << "\n";
                continue;
            }
            break;
        }

        if (user_input <= 0) {
            exit_program = true;
            break;
        }

        CLICK_DELAY = user_input;

        on_click_setup();
        cout << "Готово к работе" << "\n";
        cout << "= - Включить кликер" << "\n";
        cout << "- - Остановить кликер и изменить задержку" << "\n";
        cout << "home - Полный выход из программы\n" << "\n";

        thread hotkey_thread(on_press_keyboard);
        hotkey_thread.join();
    }

    exit_program = true;
    if (click_thread.joinable()) {
        click_thread.join();
    }

    cout << "Программа полностью закрыта.";
    timeEndPeriod(1);
    return 0;
}
