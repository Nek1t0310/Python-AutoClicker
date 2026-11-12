#include <windows.h>
#include <iostream>
#include <mmsystem.h>
#include <thread>
// #include <chrono>
#include<atomic>
// #pragma comment(lib, "winmm.lib") <- для компилятора MSVC
using namespace std;

namespace Mouse {
    enum class Button {
        Left,
        Right
    };

    void PressLeft() {
        INPUT in = { 0 };
        in.type = INPUT_MOUSE;
        in.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
        SendInput(1, &in, sizeof(INPUT));
    }

    void ReleaseLeft() {
        INPUT in = { 0 };
        in.type = INPUT_MOUSE;
        in.mi.dwFlags = MOUSEEVENTF_LEFTUP;
        SendInput(1, &in, sizeof(INPUT));
    }

    void PressRight() {
        INPUT in = { 0 };
        in.type = INPUT_MOUSE;
        in.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN;
        SendInput(1, &in, sizeof(INPUT));
    }

    void ReleaseRight() {
        INPUT in = { 0 };
        in.type = INPUT_MOUSE;
        in.mi.dwFlags = MOUSEEVENTF_RIGHTUP;
        SendInput(1, &in, sizeof(INPUT));
    }

    void ClickLeft() {
        PressLeft();
        ReleaseLeft();
    }

    void ClickRight() {
        PressRight();
        ReleaseRight();
    }
}

const int EXIT_KEY = VK_HOME;
const int ON_KEY = VK_OEM_PLUS;
const int OFF_KEY = VK_OEM_MINUS;

bool clicking = false;
bool exit_program = false;
double CLICK_DELAY = 0.1;
double CLICK_DELAY_PRESS = 0.5;
atomic<int> mode_clicker = 0;

Mouse::Button selected_button = Mouse::Button::Left;

void clicker() {
    using namespace Mouse;

    while (!exit_program) {
        if (mode_clicker == 1) {
            if (clicking) {
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
            else {
                Sleep(100);
            }
        }
        else if (mode_clicker == 2) {
            if (clicking) {
                // нажатие кнопки мышм:
                if (selected_button == Button::Left) {
                    PressLeft();
                }
                else if (selected_button == Button::Right) {
                    PressRight();
                }

                DWORD ms_sleep_press = (DWORD)(CLICK_DELAY_PRESS * 1000.0);
                Sleep(ms_sleep_press);

                // реализация кнопки мыши:
                if (selected_button == Button::Left) {
                    ReleaseLeft();
                }
                else if (selected_button == Button::Right) {
                    ReleaseRight();
                }

                DWORD ms_sleep_2 = (DWORD)(CLICK_DELAY * 1000.0);
                Sleep(ms_sleep_2);
            }
            else {
                Sleep(100);
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

    cout << "Нажмите кнопку мыши (прям на экране) для выбрра" << "\n";

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
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    HANDLE hInput = GetStdHandle(STD_INPUT_HANDLE);
    DWORD prev_mode;
    GetConsoleMode(hInput, &prev_mode);
    SetConsoleMode(hInput, prev_mode & ~ENABLE_QUICK_EDIT_MODE);

    timeBeginPeriod(1);
    thread click_thread(clicker);

    while (!exit_program) {
        cout << "Выберете режим кликов: " << "\n";
        cout << "1 - обычные клики" << "\n";
        cout << "2 - клики с интервалом(зажатие клавиши)" << "\n";

        int user_click_choice;

        while (true) {
            cout << "Выберете режим: ";
            cin >> user_click_choice;

            if (cin.fail()) {
                cin.clear();
                cin.ignore(10000, '\n');
                cout << "Ошибка, введите число. Установлена задержка по умолчанию: 0.1 сек." << "\n";
                continue;
            }
            else if (user_click_choice != 1 && user_click_choice != 2) {
                cout << "Ошибка, выберете 1 из 2 режимов!" << endl;
                continue;
            }
            break;
        }

        mode_clicker = user_click_choice;

        cout << "===========================" << "\n";
        cout << "===Настройки Автокликера===" << "\n";
        cout << "===========================" << "\n";

        if (user_click_choice == 1) {
            double user_input;

            while (true) {
                cout << "Введите задержку в секундах или 0 для выхода: " << "\n";
                cin >> user_input;

                if (cin.fail()) {
                    cin.clear();
                    cin.ignore(10000, '\n');
                    cout << "Ошибка, введите число." << "\n";
                    continue;
                }
                break;
            }

            if (user_input <= 0) {
                exit_program = true;
                break;
            }

            CLICK_DELAY = user_input;
        }

        else if (user_click_choice == 2) {
            double user_input_2;

            while (true) {
                cout << "Введите задержку в секундах между зажатиями(2 режим) или 0 для выхода: " << "\n";
                cin >> user_input_2;

                if (cin.fail()) {
                    cin.clear();
                    cin.ignore(10000, '\n');
                    cout << "Ошибка, введите число." << "\n";
                    continue;
                }
                break;
            }
            
            if (user_input_2 <= 0) {
                exit_program = true;
                break;
            }

            CLICK_DELAY = user_input_2;

            double user_input_press;

            while (true) {
                cout << "Введите время зажатия кнопки мыши(2 режим) или всё таки 0 для выхода: " << "\n";
                cin >> user_input_press;

                if (cin.fail()) {
                    cin.clear();
                    cin.ignore(10000, '\n');
                    cout << "Ошибка, введите число." << "\n";
                    continue;
                }
                break;
            }

            if (user_input_press <= 0) {
                exit_program = true;
                break;
            }

            CLICK_DELAY_PRESS = user_input_press;
        }

        else {
            cout << "Ошибка, введите число. Установлена задержка по умолчанию 0.1 сек." << endl;
            cout << "Для второго режима задержка в 0.5 секунд." << endl;
            CLICK_DELAY = 0.1;
            CLICK_DELAY_PRESS = 0.5;
        }

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
