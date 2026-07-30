import time
import random
import threading
import tkinter as tk
from pygame.mixer import init, Sound

muted = False
count = 0
click_count = 0
click_time = 1
click_stat = 0
test_started = False
start_time = 0
pressed = False
ready_for_test = False
result_buffer_stats = ""
result_buffer_text = ""

BG_MAIN = "#121212"       # Глубокий «угольный» фон для всего окна
BG_FRAME = "#1A1A1A"      # Графитовый фон для рабочего фрейма
MATRIX_GREEN = "#00FF66"  # Сочный неоновый зелёный (цвет активности)
DARK_GREEN = "#1A3322"    # Темно-зелёный для фона кнопок
ALERT_RED = "#FF3333"     # Сдержанный красный для кнопки сброса
DARK_GREY = "#1e1e1e"     # Тёмно серый цвет для фона

init()
click_sound = Sound("sounds/click_sound.mp3")
clean_sound = Sound("sounds/clean_sound.mp3")

def result_menu():
    global count, click_count, result_buffer_stats, result_buffer_text, click_stat

    result_window = tk.Toplevel(root)
    result_window.config(bg=DARK_GREY)
    result_window.title("Окно с результатами")
    result_window.geometry("700x500")
    result_window.minsize(600, 450)
    result_window.grab_set()
    result_window.focus_set()

    picture_label = tk.Label(result_window,
                             #height=15,
                             #width=30,
                             bg="black",
                             font="Arial 20",
                             )
    picture_label.pack(pady=(10, 0))

    if click_stat > 35.0:
        photo = random.choice(cheat_clicks_photo)
        picture_label.config(image=photo)
        picture_label.image = photo
        result_buffer_text = random.choice(cheat_clicks)

    elif click_stat <= 6.0:
        photo = random.choice(low_clicks_photo)
        picture_label.config(image=photo)
        picture_label.image = photo
        result_buffer_text = random.choice(low_clicks)

    elif 6 < click_stat <= 10:
        photo = random.choice(normal_clicks_photo)
        picture_label.config(image=photo)
        picture_label.image = photo
        result_buffer_text = random.choice(normal_clicks)

    elif 10 < click_stat <= 35:
        photo = random.choice(high_clicks_photo)
        picture_label.config(image=photo)
        picture_label.image = photo
        result_buffer_text = random.choice(high_clicks)

    attribute_label = tk.Label(result_window, 
                                font="Arial 20",
                                bg=DARK_GREEN,
                                foreground=MATRIX_GREEN,
                                text=result_buffer_text,
                                relief="raised"
                               )
    attribute_label.pack(pady=10)

    results_label = tk.Label(result_window,
                             font="Arial 20",
                             bg=DARK_GREEN,
                             foreground=MATRIX_GREEN,
                             text=result_buffer_stats,
                             relief="raised"
                             )
    results_label.pack(pady=5)

def on_click():
    global click_count, test_started, start_time, ready_for_test, pressed, result_buffer_stats, click_stat
    while True:
        if pressed:
            pressed = False
            if not test_started:
                test_started = True
                start_time = time.perf_counter()
                # print("Тест запущен, считаем клики за секунду...")
            
            click_count += 1

        if test_started:
            if click_time == 1:
                if time.perf_counter() - start_time >= click_time:
                    result.config(text=f"Сокрость: {click_count} CPS")
                    result_buffer_stats = f"Скорость: {click_count} CPS"
                    # print("РЕЗУЛЬТАТ ТЕСТА: ")
                    # print(f"Сокрость: {click_count} CPS")
                    button_click.config(state="disabled")
                    click_stat = click_count

                    result_menu()

                    click_count = 0
                    test_started = False
            else:
                if time.perf_counter() - start_time >= click_time:
                    click_stat = click_count / click_time
                    result.config(text=f"Скорость: {click_count} за {click_time} секунд\n" 
                                  + f"Примерно: {click_stat:.2f} CPS")
                    result_buffer_stats = f"Скорость: {click_count} за {click_time} секунд\n" + f"Примерно: {click_stat:.2f} CPS"
                    # print("РЕЗУЛЬТАТ ТЕСТА: ")
                    # print(f"Сокрость: {click_count} за {click_time} секунд")
                    # print(f"Примерно: {click_stat:.2f} CPS")
                    button_click.config(state="disabled")

                    result_menu()
                
                    click_count = 0
                    test_started = False

        if test_started:
            time.sleep(0.001)
        else:
            time.sleep(0.1)

def clicker():
    global count, ready_for_test, pressed
    count += 1
    click.config(text=count)
    pressed = True
    ready_for_test = True

    if not muted:
        click_sound.play()

def clean():
    global count, text_of_clicks, muted
    count = 0
    click.config(text=count)
    text_of_clicks = "Ожидание кликов..."
    result.config(text=text_of_clicks)
    button_click.config(state="normal")

    if not muted:
        clean_sound.play()

def plus_button():
    global click_time
    click_sound.play()
    if click_time < 15:
        click_time += 1
        entry_label_time.config(text=click_time)
        
def minus_button():
    global click_time
    click_sound.play()
    if click_time > 1:
        click_time -= 1
        entry_label_time.config(text=click_time)

def switch_sound():
    global muted
    if not muted:
        muted = True
        sound_button.config(image=image_sound_off)
        #sound_button.image = image_sound_off
    else:
        muted = False
        sound_button.config(image=image_sound_on)
        #sound_button.image = image_sound_on
        
root = tk.Tk()
root.title("Счётчик CPS")
root.geometry("700x600")
root.minsize(500, 500)
root.config(bg="#1e1e1e")
icon = tk.PhotoImage(file="icons/icon_2.png")
root.iconphoto(True, icon)
image_sound_on = tk.PhotoImage(file="icons/icon_sound.png").subsample(16, 16)
image_sound_off = tk.PhotoImage(file="icons/icon_silent.png").subsample(16, 16)


low_clicks = [
    "Скорость улитки.",
    "Слишком медленно.",
    "Тотальный застой.",
    "Руки клешни.",
    "Нужно тренироваться."
]

low_clicks_photo = [
    tk.PhotoImage(file="images_low/low.png"),
    tk.PhotoImage(file="images_low/low_2.png"),
    tk.PhotoImage(file="images_low/low_3.png"),
    tk.PhotoImage(file="images_low/low_4.png"),
    tk.PhotoImage(file="images_low/low_5.png")
]

normal_clicks = [
    "Норма достигнута.",
    "Темп стабилен.",
    "Молодец, неплохо!",
    "Хорошая скорость.",
    "Показатели в норме."
]

normal_clicks_photo = [
    tk.PhotoImage(file="images_normal/respect.png"),
    tk.PhotoImage(file="images_normal/respect_2.png"),
    tk.PhotoImage(file="images_normal/respect_3.png"),
    tk.PhotoImage(file="images_normal/respect_4.png"),
    tk.PhotoImage(file="images_normal/respect_5.png")
]

high_clicks = [
    "Легенда.",
    "Красавчик!",
    "Киборг",
    "Отличная работа!",
    "Дикая скорость!"
]

high_clicks_photo = [
    tk.PhotoImage(file="images_high/hight.png"),
    tk.PhotoImage(file="images_high/hight_2.png"),
    tk.PhotoImage(file="images_high/hight_3.png"),
    tk.PhotoImage(file="images_high/hight_4.png"),
    tk.PhotoImage(file="images_high/hight_5.png")
]

cheat_clicks = [
    "Не жульничай!",
    "Автокликер, чувак.",
    "Клоун обнаружен",
    "Убери скрипты.",
    "Недостойный..."
]

cheat_clicks_photo = [
    tk.PhotoImage(file="images_cheat/cheat.png"),
    tk.PhotoImage(file="images_cheat/cheat_2.png"),
    tk.PhotoImage(file="images_cheat/cheat_3.png"),
    tk.PhotoImage(file="images_cheat/cheat_4.png"),
    tk.PhotoImage(file="images_cheat/cheat_5.png")
]

general_frame = tk.Frame(root,
                      height=430,
                      width=450,
                      bg=BG_MAIN
                      )
general_frame.pack(expand=True)

top_menu_frame = tk.Frame(general_frame, 
                       height=60,
                       width=450,
                       bg=BG_FRAME,
                       relief="groove",
                       borderwidth=3,
                       highlightbackground="white"
                       )
top_menu_frame.pack(side="top", pady=(0, 5))
top_menu_frame.pack_propagate(False)

sound_button = tk.Button(top_menu_frame,
                          image=image_sound_on,
                          bg=DARK_GREEN,
                          activebackground=MATRIX_GREEN,
                          command=switch_sound
                          )
sound_button.pack(side="left", padx=(15, 0))

entry_time = tk.Label(top_menu_frame,
                   font="Arial 20",
                   fg=MATRIX_GREEN,
                   bg=DARK_GREEN,
                   width=14,
                   justify="center",
                   text="Выставите время:"
                   )
entry_time.pack(side="left", padx=(10, 0), pady=5) # 60

entry_button_minus = tk.Button(top_menu_frame,
                              height=1,
                              width=2,
                              text="-",
                              font="Arial 12 bold",
                              activebackground=MATRIX_GREEN,
                              activeforeground=BG_FRAME,
                              bg=DARK_GREEN,
                              fg=MATRIX_GREEN,
                              command=minus_button
                              )
entry_button_minus.pack(side="left", padx=(15, 5))

entry_label_time = tk.Label(top_menu_frame,
                            text=click_time,
                            height=1,
                            width=2,
                            font="Arial 20 bold",
                            highlightbackground="grey",
                            bg=BG_FRAME,
                            fg=MATRIX_GREEN,
                            borderwidth=3,
                            relief="groove"
                            )
entry_label_time.pack(side="left", padx=5)

entry_button_plus = tk.Button(top_menu_frame,
                              text="+",
                              height=1,
                              width=2,
                              font="Arial 12 bold",
                              activebackground=MATRIX_GREEN,
                              activeforeground=BG_FRAME,
                              bg=DARK_GREEN,
                              fg=MATRIX_GREEN,
                              command=plus_button
                              )
entry_button_plus.pack(side="left", padx=5)

main_frame = tk.Frame(general_frame, 
                   width=450, 
                   height=380, 
                   bg="#1A1A1A",
                   relief="groove",
                   borderwidth=3,
                   highlightbackground="black"
                   )
main_frame.pack(expand=True)
main_frame.pack_propagate(False)

click = tk.Label(main_frame, 
              text="0",
              font="Arial 30",
              relief="ridge",
              borderwidth=3,
              highlightbackground="black",
              bg=BG_FRAME,
              fg=MATRIX_GREEN
              )
click.pack(pady="10")

button_click = tk.Button(main_frame, 
             text="Кликай!", 
             padx="20",
             pady="20",
             font="Arial 20",
             relief="sunken",
             fg=MATRIX_GREEN,
             bg=DARK_GREEN,
             activebackground=MATRIX_GREEN,
             activeforeground=BG_FRAME,
             command=clicker
             )
button_click.pack(pady="10")

result = tk.Label(main_frame,
               text="Ожидание кликов...",
               font="Arial 20",
               relief="groove",
               borderwidth=3,
               highlightbackground="#2A2A2A",
               bg="#151515",
               fg=MATRIX_GREEN
               )
result.pack(pady="10")

button_clean = tk.Button(main_frame, 
             text="Очистить", 
             padx="20",
             pady="10",
             font="Arial 16",
             bg=ALERT_RED,
             fg="white",
             relief="sunken",
             command=clean
             )
button_clean.pack(pady="10")

click_thread = threading.Thread(target=on_click, daemon=True)
click_thread.start()

root.mainloop()
