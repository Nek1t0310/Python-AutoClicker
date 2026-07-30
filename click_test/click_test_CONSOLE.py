import time
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode

click_count = 0
test_started = False
start_time = 0

exit_program = False
ready_for_test = False

def on_click(_, __, button, pressed):
    global click_count, test_started, start_time, ready_for_test

    if pressed and ready_for_test:
        if not test_started:
            test_started = True
            start_time = time.perf_counter()
            print("Тест запущен, считаем клики за секунду...")
        
        click_count += 1

        if time.perf_counter() - start_time >= 1.0:
            print("РЕЗУЛЬТАТ ТЕСТА: ")
            print(f"Сокрость: {click_count} CPS")

            click_count = 0
            test_started = False
            ready_for_test = False

            print("Для нового теста нажмите: 1")
            print("Для полного выхода нажмите: 2 ")

def on_press(key):
    global exit_program, ready_for_test

    if key == KeyCode(char="2"):
        print("Программа завершена.")
        exit_program = True
        ready_for_test = False
        return False

    elif key == KeyCode(char="1"):
        if not ready_for_test:
            ready_for_test = True
            print("Клик тест готов, считаем клики за секунду...")

keyboard_listener = KeyboardListener(on_press=on_press)
keyboard_listener.start()

mouse_listener = MouseListener(on_click=on_click)
mouse_listener.start()

print("Клик тест готов!")
print("Нажмите 1 что бы запустить тест ")
print("Нажмите 2 что бы выключить программу")

while not exit_program:
    time.sleep(0.1)

mouse_listener.stop()
keyboard_listener.stop()
print("Программа успешно остановлена.")
