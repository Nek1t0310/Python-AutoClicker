import time
import queue
import ctypes
import threading
from pynput.mouse import Button, Controller, Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode

ON_KEY = KeyCode(char="=")
OFF_KEY = KeyCode(char="-")

mouse = Controller()
clicking = False
exit_program = False
click_event = threading.Event()
mode_queue = queue.Queue()

SELECTED_BUTTON = Button.left
current_mode = None

def clicker(q):
    mode = None

    while not exit_program:
        if not q.empty():
            mode = q.get()

        if mode is None:
            time.sleep(0.1)
            continue

        if mode == 1:
            if clicking:
                #start_time = time.perf_counter()
                mouse.press(SELECTED_BUTTON)
                mouse.release(SELECTED_BUTTON)
                # while time.perf_counter() - start_time < CLICK_DELAY:
                #     pass
                click_event.wait(timeout=CLICK_DELAY)
            else:
                time.sleep(0.1)
        elif mode == 2:
            if clicking:
                mouse.press(SELECTED_BUTTON)
                click_event.wait(timeout=CLICK_DELAY_PRESS)
                mouse.release(SELECTED_BUTTON)

                click_event.wait(timeout=CLICK_DELAY)
            else:
                time.sleep(0.1)
            

def on_press_keyboard(key):
    global clicking, exit_program

    if key == Key.home:
        print("Программа завершена.")
        clicking = False
        exit_program = True
        return False
    
    elif key == ON_KEY:
        if not clicking:
            clicking = True
            print(f"Автокликер: Включен ({'ЛКМ' if SELECTED_BUTTON == Button.left else 'ПКМ'})")
        else:
            clicking = False
            print("Автокликер: Выключен(Пауза)")

    elif key == OFF_KEY:
        clicking = False
        print("Автокликер: Остановлен. Возврат к настройкам...")
        return False
    
def on_click_setup(_, __, button, pressed):
    global SELECTED_BUTTON

    if pressed:
        if button == Button.left:
            SELECTED_BUTTON = Button.left
            print("Выбрана левая кнопка мыши(ЛКМ)")
            return False
        elif button == Button.right:
            SELECTED_BUTTON = Button.right
            print("Выбрана правая кнопка мыши (ПКМ)")
            return False

winmm =  ctypes.windll.winmm
winmm.timeBeginPeriod(1)
click_thread = threading.Thread(target=clicker, args=(mode_queue, ), daemon=True)
click_thread.start()

while not exit_program:
    print("Выберете режим кликов: ")
    print("1 - обычные клики")
    print("2 - клики с интервалом(зажатие клавиши)")

    while True:
        try:
            user_click_choice = int(input("Выберете режим: "))
            if user_click_choice in [1, 2]:
                break
            else:
                print("Введите число 1 или 2")
        except ValueError:
            print("Ошибка, введите целове число(1 или 2).")

    mode_queue.put(user_click_choice)

    print("===========================")
    print("===Настройки Автокликера===")
    print("===========================")
    try:
        if user_click_choice == 1:
            user_input = input("Введите задержку в секундах или exit для выхода: ")

            if user_input.lower() == "exit":
                exit_program = True
                break

            CLICK_DELAY = float(user_input)
        elif user_click_choice == 2:
            user_input_2 = input("Введите задержку в секундах между зажатиями(2 режим) или exit для выхода: ")

            if user_input_2.lower() == "exit":
                exit_program = True
                break

            CLICK_DELAY = float(user_input_2)

            uset_input_press = input("Введите время зажатия кнопки мыши в секундахили всё так же exit для выхода: ")

            if uset_input_press.lower() == "exit":
                exit_program = True
                break

            CLICK_DELAY_PRESS = float(uset_input_press)

    except ValueError:
        print("Ошибка, введите число. Установлена задержка по умолчанию: 0.1 сек.")
        print("Для второго режима задержка в 0.5 секунд.")
        CLICK_DELAY = 0.1
        CLICK_DELAY_PRESS = 0.5       

    print("Нажмите кнопку мыши(прям на экране) для выбора")

    with MouseListener(on_click=on_click_setup) as mouse_listener:
        mouse_listener.join()

    print("\nГотово к работе")
    print("= - Включить кликер")
    print("- - Остановить кликер и изменить задержку")
    print("home - Полный выход из программы\n")

    with KeyboardListener(on_press=on_press_keyboard) as keyboard_listener:
        keyboard_listener.join()

winmm.timeEndPeriod(1)
print("Программа успешно закрыта.")
