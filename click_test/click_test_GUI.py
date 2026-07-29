import time
import threading
import tkinter as tk
from pygame.mixer import init, Sound

click_count = 0
click_time = 1
test_started = False
start_time = 0
pressed = False
ready_for_test = False

BG_MAIN = "#121212"       # Глубокий «угольный» фон для всего окна
BG_FRAME = "#1A1A1A"      # Графитовый фон для рабочего фрейма
MATRIX_GREEN = "#00FF66"  # Сочный неоновый зелёный (цвет активности)
DARK_GREEN = "#1A3322"    # Темно-зелёный для фона кнопок
ALERT_RED = "#FF3333"     # Сдержанный красный для кнопки сброса
DARK_GREY = "#1e1e1e"     # Тёмно серый цвет для фона

init()
click_sound = Sound("click_sound.mp3")
clean_sound = Sound("clean_sound.mp3")

count = 0

def on_click():
    global click_count, test_started, start_time, ready_for_test, pressed
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
                    result.config(text=f"Скорость: {click_count} CPS")
                    # print("РЕЗУЛЬТАТ ТЕСТА: ")
                    # print(f"Сокрость: {click_count} CPS")
                    button_click.config(state="disabled")

                    click_count = 0
                    test_started = False
            else:
                if time.perf_counter() - start_time >= click_time:
                    click_stat = click_count / click_time
                    result.config(text=f"Скорость: {click_count} за {click_time} секунд\n" 
                                  + f"Примерно: {click_stat:.2f} CPS")
                    # print("РЕЗУЛЬТАТ ТЕСТА: ")
                    # print(f"Сокрость: {click_count} за {click_time} секунд")
                    # print(f"Примерно: {click_stat:.2f} CPS")
                    button_click.config(state="disabled")
                
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
    click_sound.play()
    pressed = True
    ready_for_test = True

def clean():
    global count, text_of_clicks
    count = 0
    click.config(text=count)
    text_of_clicks = "Ожидание кликов..."
    result.config(text=text_of_clicks)
    button_click.config(state="normal")
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

root = tk.Tk()
root.title("Счётчик CPS")
root.geometry("700x600")
root.minsize(500, 500)
root.config(bg="#1e1e1e")
icon = tk.PhotoImage(file="icon_2.png")
root.iconphoto(True, icon)

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

entry_time = tk.Label(top_menu_frame,
                   font="Arial 20",
                   fg=MATRIX_GREEN,
                   bg=DARK_GREEN,
                   width=14,
                   justify="center",
                   text="Выставите время:"
                   )
entry_time.pack(side="left", padx=(60, 0), pady=5)

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
