import time
import json
import ctypes
import random
import winsound
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pynput.keyboard import KeyCode
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener as KeyboardListener, Key

ACTIVATE_KEY_1 = Key.f8
ACTIVATE_KEY_2 = Key.f9
CHANGED_ACTIVATE_KEY_1 = Key.f8
CHANGED_ACTIVATE_KEY_2 = Key.f9
ACTIVE_BUTTON = 1
SETTING_FILE = "settings.json"

normal_key_name_1 = str(ACTIVATE_KEY_1).replace("Key.", "").replace("'", "").upper()
normal_key_name_2 = str(ACTIVATE_KEY_2).replace("Key.", "").replace("'", "").upper()

mouse = Controller()
clicking = False
stop_click = False
is_setting_hotkey_1 = False
is_setting_hotkey_2 = False
random_activate = False

first_mouse = True
second_mouse = False

on_press_change = False
click_event = threading.Event()
winmm = ctypes.windll.winmm

SELECTED_BUTTON = Button.left
SELECTED_BUTTON_2 = Button.left
CLICK_DELAY = 0.01
RANDOM_OFFSET_VALUE = 0

BUTTON_MAP = {
    "Left": Button.left,
    "Right": Button.right,
    "Middle": Button.middle
}

def hotkeys_any_layout(event):
    if event.widget.winfo_class() != "Entry":
        return

    hotkeys = {
        65: "<<SelectAll>>",  # A
        67: "<<Copy>>",       # C
        86: "<<Paste>>",      # V
        88: "<<Cut>>",        # X
        90: "<<Undo>>"        # Z (В tk.Entry ctrl + z НЕ РАБОТАЕТ, оставил для приличия)
    }
    
    if event.keycode in hotkeys:
        event.widget.event_generate(hotkeys[event.keycode])
        return "break"


def smart_focus_clear(event):
    if event.widget.winfo_class() not in ("Entry", "TCombobox"):
        root.focus()


def validate_entry(P):
    if len(P) > 7:
        return False
    elif P == "":
        return True
    elif P.isdigit():
        return True
    else:
        winsound.MessageBeep(winsound.MB_OK)
        return False


def validate_entry_2(P):
    if len(P) > 3:
        return False
    elif P == "":
        return True
    elif P.isdigit():
        return True
    else:
        winsound.MessageBeep(winsound.MB_OK)
        return False


def setup_button_1(event):
    global SELECTED_BUTTON
    global BUTTON_MAP

    user_choice = mouse_choice_label_1.get()
    SELECTED_BUTTON = BUTTON_MAP[user_choice]
    #print(f"1 кнопка мыши изменена на: {user_choice}")


def setup_button_2(event):
    global SELECTED_BUTTON_2
    global BUTTON_MAP

    user_choice_2 = mouse_choice_label_2.get()
    SELECTED_BUTTON_2 = BUTTON_MAP[user_choice_2]
    #print(f"2 кнопка мыши изменена на: {user_choice_2}")


def click_delay():
    global RANDOM_OFFSET_VALUE

    mins = int(min_entry.get() or 0)
    seconds = int(sec_entry.get() or 0)
    milliseconds = int(millisec_entry.get() or 0)

    if random_activate:
        RANDOM_OFFSET_VALUE = int(offset_choice_label.get() or 0)

    total_time = (mins * 60) + seconds + (milliseconds / 1000)
    return total_time


def clicker():
    global ACTIVE_BUTTON
    while not stop_click:
        if clicking:
            if ACTIVE_BUTTON == 1 and first_mouse:
                current_button = SELECTED_BUTTON
            elif ACTIVE_BUTTON == 2 and second_mouse:
                current_button = SELECTED_BUTTON_2
            else:
                time.sleep(0.01)
                continue

            mouse.press(current_button)
            mouse.release(current_button)

            current_delay = CLICK_DELAY

            if random_activate:
                offset_delay = RANDOM_OFFSET_VALUE / 1000
                current_delay += random.uniform(-offset_delay, offset_delay)

                if current_delay < 0.001:
                    current_delay = 0.001

            click_event.wait(timeout=current_delay)
        else:
            time.sleep(0.1)


def hotkey_choice_1():
    global on_press_change
    global is_setting_hotkey_1
    global is_setting_hotkey_2

    is_setting_hotkey_1 = True
    is_setting_hotkey_2 = False
    on_press_change = True
    label_choice.config(text="Choose key")


def hotkey_choice_2():
    global on_press_change
    global is_setting_hotkey_1
    global is_setting_hotkey_2

    is_setting_hotkey_1 = False
    is_setting_hotkey_2 = True
    on_press_change = True
    label_choice_2.config(text="Choose key")


def open_settings():
    setting_window.deiconify()
    setting_window.grab_set()
    setting_window.focus_set()


def close_settings():
    global is_setting_hotkey_1
    global is_setting_hotkey_2
    global normal_key_name_1
    global normal_key_name_2
    global on_press_change
    global ACTIVATE_KEY_1
    global CHANGED_ACTIVATE_KEY_1
    global ACTIVATE_KEY_2
    global CHANGED_ACTIVATE_KEY_2

    setting_window.grab_release()
    setting_window.withdraw()

    if CHANGED_ACTIVATE_KEY_1 is not None:
        ACTIVATE_KEY_1 = CHANGED_ACTIVATE_KEY_1
        normal_key_name_1 = str(ACTIVATE_KEY_1).replace("Key.", "").replace("'", "").upper()
        label_choice.config(text=normal_key_name_1)
        button_start.config(text=f"Start({normal_key_name_1})\nButton 1")

    if CHANGED_ACTIVATE_KEY_2 is not None:
        ACTIVATE_KEY_2 = CHANGED_ACTIVATE_KEY_2
        normal_key_name_2 = str(ACTIVATE_KEY_2).replace("Key.", "").replace("'", "").upper()
        label_choice_2.config(text=normal_key_name_2)
        button_start_2.config(text=f"Start({normal_key_name_2})\nButton 2")

    is_setting_hotkey_1 = False
    is_setting_hotkey_2 = False
    on_press_change = False


def close_setting_no_changes():
    global is_setting_hotkey_1
    global is_setting_hotkey_2
    global normal_key_name_1
    global normal_key_name_2
    global on_press_change
    global CHANGED_ACTIVATE_KEY_1
    global CHANGED_ACTIVATE_KEY_2

    setting_window.grab_release()
    setting_window.withdraw()

    label_choice.config(text=normal_key_name_1)
    label_choice_2.config(text=normal_key_name_2)
    button_start.config(text=f"Start({normal_key_name_1})\nButton 1")
    button_start_2.config(text=f"Start({normal_key_name_2})\nButton 2")

    CHANGED_ACTIVATE_KEY_1 = ACTIVATE_KEY_1
    CHANGED_ACTIVATE_KEY_2 = ACTIVATE_KEY_2

    is_setting_hotkey_1 = False
    is_setting_hotkey_2 = False
    on_press_change = False


def on_press_keyboard(key):
    global clicking
    global stop_click
    global first_mouse
    global second_mouse
    global is_setting_hotkey_1
    global is_setting_hotkey_2
    global on_press_change
    global CLICK_DELAY
    global ACTIVE_BUTTON
    global ACTIVATE_KEY_1
    global CHANGED_ACTIVATE_KEY_1
    global ACTIVATE_KEY_2
    global CHANGED_ACTIVATE_KEY_2

    active_hotkey()

    if (is_setting_hotkey_1 or is_setting_hotkey_2) and on_press_change: 
        if key in(Key.shift, Key.shift_r, Key.ctrl, Key.ctrl_l, Key.ctrl_r, Key.alt, Key.alt_l, Key.alt_r):
            return

        key_name = str(key).replace("Key.", "").replace("'", "").upper()

        if is_setting_hotkey_1:
            CHANGED_ACTIVATE_KEY_1 = key
            label_choice.config(text=key_name)

        elif is_setting_hotkey_2:
            CHANGED_ACTIVATE_KEY_2 = key
            label_choice_2.config(text=key_name)

        on_press_change = False
        return

    if is_setting_hotkey_1 or is_setting_hotkey_2:
        return

    # получаем виртуальный код нажатой клавиши
    try:
        if isinstance(key, Key):
            pressed_vk = key.value.vk
        else:
            pressed_vk = key.vk
    except AttributeError:
        return

    # получаем виртуальный код клавиши активации
    #1
    try:
        if isinstance(ACTIVATE_KEY_1, Key):
            target_vk_1 = ACTIVATE_KEY_1.value.vk
        else:
            target_vk_1 = ACTIVATE_KEY_1.vk
    except AttributeError:
        target_vk_1 = 119 # f8
    #2
    try:
        if isinstance(ACTIVATE_KEY_2, Key):
            target_vk_2 = ACTIVATE_KEY_2.value.vk
        else:
            target_vk_2 = ACTIVATE_KEY_2.vk
    except AttributeError:
        target_vk_2 = 120 # f9


    # сравниваем коды нажатой клавиши и клавиши активации
    #1
    if pressed_vk == target_vk_1 and first_mouse:
        #если у нас была активна эта клавиша выключаем её
        if ACTIVE_BUTTON == 1 and clicking:
            clicking = False
        #иначе переключаем её на клики
        else:
            ACTIVE_BUTTON = 1
            if not clicking:
                CLICK_DELAY = click_delay()
                clicking = True
                #print("Кликер включен(1 Кнопка)")
            return

    #2
    if pressed_vk == target_vk_2 and second_mouse:
        #если у нас была активна эта клавиша выключаем её
        if ACTIVE_BUTTON == 2 and clicking:
            clicking = False
        #иначе переключаем её на клики
        else:
            ACTIVE_BUTTON = 2
            if not clicking:
                CLICK_DELAY = click_delay()
                clicking = True
                #print("Кликер включен(2 Кнопка)")
        return

def random_info():
    messagebox.showinfo("About Random Offset", "The selected interval (e.g., 20 ms) will vary dynamically from -20 ms to +20 ms. This random deviation helps bypass basic anti-cheat checks during Minecraft PvP :)")


def switch_random():
    global random_activate

    if random_offset.get() == 1:
        random_activate = True
        #print("Рандом включен")
    else:
        random_activate = False
        #print("Рандом выключен")


def active_hotkey():
    global first_mouse
    global second_mouse

    if first_mouse == True:
        button_start.config(state="normal")
    else:
        button_start.config(state="disabled")

    if second_mouse == True:
        button_start_2.config(state="normal")
    else:
        button_start_2.config(state="disabled")


def switch_button_1():
    global first_mouse

    if first_mouse_choice.get() == 1:
        first_mouse = True
        #print("1 кнопка включена")
    else:
        first_mouse = False
        #print("1 кнопка выключена")
    active_hotkey()


def switch_button_2():
    global second_mouse
    
    if second_mouse_choice.get() == 1:
        second_mouse = True
        #print("2 кнопка включена")
    else:
        second_mouse = False
        #print("2 кнопка выключена")
    active_hotkey()


def sync_selected_buttons():
    global BUTTON_MAP
    global SELECTED_BUTTON
    global SELECTED_BUTTON_2

    user_choice = mouse_choice_label_1.get()
    SELECTED_BUTTON = BUTTON_MAP[user_choice]
    user_choice_2 = mouse_choice_label_2.get()
    SELECTED_BUTTON_2 = BUTTON_MAP[user_choice_2]


def save_settings():
    global ACTIVATE_KEY_1
    global ACTIVATE_KEY_2

    #1 кнопка мыши
    #----------------------------------------------------------
    # сохраняем имя клавиши
    if hasattr(ACTIVATE_KEY_1, 'name') and ACTIVATE_KEY_1.name is not None:
        key_to_save = ACTIVATE_KEY_1.name
    elif hasattr(ACTIVATE_KEY_1, 'char') and ACTIVATE_KEY_1.char is not None:
        key_to_save = ACTIVATE_KEY_1.char
    else:
        key_to_save = str(normal_key_name_1).lower() 

    # сохраняем виртуальный код клавиши
    try:
        if isinstance(ACTIVATE_KEY_1, Key):
            vk_to_save = ACTIVATE_KEY_1.value.vk
        else:
            vk_to_save = ACTIVATE_KEY_1.vk
    except AttributeError:
        vk_to_save = 119

    #2 кнопка мыши
    #----------------------------------------------------------
    # сохраняем имя клавиши
    if hasattr(ACTIVATE_KEY_2, 'name') and ACTIVATE_KEY_2.name is not None:
        key_to_save_2 = ACTIVATE_KEY_2.name
    elif hasattr(ACTIVATE_KEY_2, 'char') and ACTIVATE_KEY_2.char is not None:
        key_to_save_2 = ACTIVATE_KEY_2.char
    else:
        key_to_save_2 = str(normal_key_name_2).lower() 

    # сохраняем виртуальный код клавиши
    try:
        if isinstance(ACTIVATE_KEY_2, Key):
            vk_to_save_2 = ACTIVATE_KEY_2.value.vk
        else:
            vk_to_save_2 = ACTIVATE_KEY_2.vk
    except AttributeError:
        vk_to_save_2 = 120

    save_data = {
        "min": min_entry.get(),
        "sec": sec_entry.get(),
        "millisec": millisec_entry.get(),
        "activate_random": random_activate,
        "random_offset": offset_choice_label.get(),
        "selected_button": mouse_choice_label_1.get(),
        "selected_button_2": mouse_choice_label_2.get(),
        "activate_button_1": first_mouse,
        "activate_button_2": second_mouse,
        "selected_hotkey": key_to_save,
        "selected_hotkey_vk": vk_to_save,
        "selected_hotkey_2": key_to_save_2,
        "selected_hotkey_vk_2": vk_to_save_2
    }

    with open(SETTING_FILE, "w", encoding="utf-8") as file:
        json.dump(save_data, file, indent=4, ensure_ascii=False)

    #print("Данные сохранены.")
    root.destroy()


def load_settings():
    global first_mouse
    global second_mouse
    global random_activate
    global normal_key_name_1
    global normal_key_name_2
    global ACTIVATE_KEY_1
    global CHANGED_ACTIVATE_KEY_1
    global ACTIVATE_KEY_2
    global CHANGED_ACTIVATE_KEY_2

    try:
        with open(SETTING_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        #Загрузка хоткея 1 кнопка
        #------------------------------------------------
        key_name = data.get("selected_hotkey", "f8")
        key_vk = data.get("selected_hotkey_vk", 119)

        if key_name is None:
            key_name = "f8"

        if key_name in Key.__members__:
            loaded_key = Key[key_name]
        else:
            loaded_key = KeyCode.from_vk(key_vk)

        ACTIVATE_KEY_1 = loaded_key
        CHANGED_ACTIVATE_KEY_1 = loaded_key
        normal_key_name_1 = key_name.replace("Key.", "").replace("'", "").upper()
        button_start.config(text=f"Start({normal_key_name_1})\nButton 1")
        label_choice.config(text=normal_key_name_1)

        #Загрузка хоткея 2 кнопка
        #------------------------------------------------
        key_name_2 = data.get("selected_hotkey_2", "f9")
        key_vk_2 = data.get("selected_hotkey_vk_2", 120)

        if key_name_2 is None:
            key_name_2 = "f9"

        if key_name_2 in Key.__members__:
            loaded_key_2 = Key[key_name_2]
        else:
            loaded_key_2 = KeyCode.from_vk(key_vk_2)

        ACTIVATE_KEY_2 = loaded_key_2
        CHANGED_ACTIVATE_KEY_2 = loaded_key_2
        normal_key_name_2 = key_name_2.replace("Key.", "").replace("'", "").upper()
        button_start_2.config(text=f"Start({normal_key_name_2})\nButton 2")
        label_choice_2.config(text=normal_key_name_2)

        #min input
        min_entry.delete(0, tk.END)
        min_entry.insert(0, data.get("min", "0"))

        #seconds input 
        sec_entry.delete(0, tk.END)
        sec_entry.insert(0, data.get("sec", "0"))

        #milliseconds input
        millisec_entry.delete(0, tk.END)
        millisec_entry.insert(0, data.get("millisec", "40"))

        #random off/on
        offset_choice_label.delete(0, tk.END)
        offset_choice_label.insert(0, data.get("random_offset", "20"))

        #saved_button_1
        saved_button = data.get("selected_button", "Left")
        mouse_choice_label_1.set(saved_button)

        #saved_button_2
        saved_button_2 = data.get("selected_button_2", "Right")
        mouse_choice_label_2.set(saved_button_2)

        first_mouse = data.get("activate_button_1", True)
        if first_mouse == True:
            first_mouse_choice.set(1)
        else:
            first_mouse_choice.set(0)

        second_mouse = data.get("activate_button_2", False)
        if second_mouse == True:
            second_mouse_choice.set(1)
        else:
            second_mouse_choice.set(0)

        random_activate = data.get("activate_random", False)
        if random_activate == True:
            random_offset.set(1)
        else:
            random_offset.set(0)

        active_hotkey()
        sync_selected_buttons()

    except FileNotFoundError:
        messagebox.showwarning(
            "Attention",
            "The settings.json file was not found!\nDefault settings will be used. The file will be created automatically upon exit."
        )

    except json.JSONDecodeError:
        messagebox.showerror(
            "File Error",
            "The settings.json file is corrupted or empty!\nThe file will be reset to default settings."
        )
    #print("Данные загруженны.")


def theme_settings():
    messagebox.showinfo("Attention", "in development")

root = tk.Tk()
root.title("Auto Clicker")
root.geometry("520x420")
root.attributes("-topmost", True)
root.resizable(False, False)
root.iconbitmap("icons/icon.ico")
vcmd = root.register(validate_entry)
vcmd_2 = root.register(validate_entry_2)
root.bind("<Control-Key>", hotkeys_any_layout)
root.bind("<Button-1>", smart_focus_clear)
root.protocol("WM_DELETE_WINDOW", save_settings)

main_frame = tk.Frame(root,
                      height=420,
                      width=600,
                      bg="lightgrey"
                      )
main_frame.pack(expand=True)
main_frame.pack_propagate(False)

#top frame
#top top frame
#===================================================
top_frame = tk.LabelFrame(main_frame, font="Arial 10", text="Click interval", height=130, width=490, bg="lightgrey")
top_frame.pack(expand=True, pady=(5, 5), padx=5)
top_frame.pack_propagate(False)

top_frame_top = tk.Frame(top_frame, height=60, width=490, bg="lightgrey")
top_frame_top.pack(side="top")
top_frame_top.pack_propagate(False)

min_entry = tk.Entry(top_frame_top,
                     relief="solid",
                     width=7,
                     validate="key",
                     validatecommand=(vcmd, "%P")
                     )
min_entry.insert(0, "0")
min_entry.pack(side="left", padx=(30, 0))

min_time = tk.Label(top_frame_top,
                    font="Arial 14",
                    text="min",
                    bg="lightgrey"
                    )
min_time.pack(side="left", padx=(5, 10))


sec_entry = tk.Entry(top_frame_top,
                     relief="solid",
                     width=7,
                     validate="key",
                     validatecommand=(vcmd, "%P")
                     )
sec_entry.insert(0, "0")
sec_entry.pack(side="left", padx=(40, 0))

sec_time = tk.Label(top_frame_top,
                     font="Arial 14",
                     text="sec",
                     bg="lightgrey"
                    )
sec_time.pack(side="left", padx=(5, 10))


millisec_entry = tk.Entry(top_frame_top,
                         relief="solid",
                         width=7,
                         validate="key",
                         validatecommand=(vcmd, "%P")
                         )
millisec_entry.insert(0, "40")
millisec_entry.pack(side="left", padx=(40, 0))

millisec_time = tk.Label(top_frame_top,
                         font="Arial 14",
                         text="milliseconds",
                         bg="lightgrey"
                         )
millisec_time.pack(side="left", padx=(5, 10))

#top bottom frame
#----------------------------------------------

bottom_frame_top = tk.Frame(top_frame, height=60, width=490, bg="lightgrey")
bottom_frame_top.pack(side="top")
bottom_frame_top.pack_propagate(False)

offset_button_information = tk.Button(bottom_frame_top,
                         height=1,
                         width=3,
                         font="Arial 12",
                         bg="lightgrey",
                         text="?",
                         relief="solid",
                         command=random_info
                         )
offset_button_information.pack(side="left", padx=(50, 0))

random_offset = tk.IntVar(value=0)
offset_button = tk.Checkbutton(bottom_frame_top,
                         text="Random Offset +-",
                         font="Arial 14",
                         relief="flat",
                         bg="lightgrey",
                         variable=random_offset,
                         command=switch_random
                        )
offset_button.pack(side="left", padx=(5, 0))

offset_choice_label = tk.Entry(bottom_frame_top,
                             font="Arial 14",
                             relief="sunken",
                             width=3,
                             validate="key",
                             validatecommand=(vcmd_2, "%P")
                            )
offset_choice_label.insert(0, "20")
offset_choice_label.pack(side="left", padx=(10, 0))

offset_time = tk.Label(bottom_frame_top,
                         font="Arial 14",
                         text="milliseconds",
                         bg="lightgrey"
                       )
offset_time.pack(side="left", padx=(5, 0))

#middle frame
#===================================================
#middle top frame
#----------------------------------------------
middle_frame = tk.LabelFrame(main_frame, font="Arial 10", text="Click options", height=120, width=490, bg="lightgrey")
middle_frame.pack(expand=True, padx=5)
middle_frame.pack_propagate(False)

top_middle_frame = tk.Frame(middle_frame, height=50, width=600, bg="lightgrey")
top_middle_frame.pack(side="top")
top_middle_frame.pack_propagate(False)

first_mouse_choice = tk.IntVar(value=0)
mouse_choice_1 = tk.Checkbutton(top_middle_frame,
                         font="Arial 14",
                         text="Mouse Button 1:",
                         bg="lightgrey",
                         relief="flat",
                         variable=first_mouse_choice,
                         command=switch_button_1
                        )
mouse_choice_1.pack(side="left", padx=(120, 0))

mouse_choice_label_1 = ttk.Combobox(top_middle_frame,
                             font="Arial 14",
                             values=["Left", "Right", "Middle"],
                             width=8,
                             state="readonly"
                            )
mouse_choice_label_1.set("Left")
mouse_choice_label_1.pack(side="left", padx=(10, 0))
mouse_choice_label_1.bind("<<ComboboxSelected>>", setup_button_1)

#middle bottom frame
#----------------------------------------------

bottom_middle_frame = tk.Frame(middle_frame, height=60, width=600, bg="lightgrey")
bottom_middle_frame.pack(side="top")
bottom_middle_frame.pack_propagate(False)

second_mouse_choice = tk.IntVar(value=0)
mouse_choice_2 = tk.Checkbutton(bottom_middle_frame,
                         font="Arial 14",
                         text="Mouse Button 2:",
                         bg="lightgrey",
                         relief="flat",
                         variable=second_mouse_choice,
                         command=switch_button_2
                        )
mouse_choice_2.pack(side="left", padx=(120, 0))

mouse_choice_label_2 = ttk.Combobox(bottom_middle_frame,
                             font="Arial 14",
                             values=["Left", "Right", "Middle"],
                             width=8,
                             state="readonly"
                            )
mouse_choice_label_2.set("Left")
mouse_choice_label_2.pack(side="left", padx=(10, 0))
mouse_choice_label_2.bind("<<ComboboxSelected>>", setup_button_2)

#bottom frame
#===================================================
#bottom top frame
#----------------------------------------------
bottom_frame = tk.LabelFrame(main_frame, font="Arial 10", text="Settings", height=150, width=490, bg="lightgrey")
bottom_frame.pack(expand=True, pady=5, padx=5)
bottom_frame.pack_propagate(False)

top_frame_bottom = tk.Frame(bottom_frame,
                             height=50,
                             width=490,
                             bg="lightgrey"
                            )
top_frame_bottom.pack(expand=True)
top_frame_bottom.pack_propagate(False)

button_start = tk.Button(top_frame_bottom,
                         height=2,
                         width=13,
                         font="Arial 12",
                         text=f"Start({normal_key_name_1})\nButton 1",
                         #command=active_hotkey
                         )
button_start.pack(side="left", padx=(110, 0))

button_start_2 = tk.Button(top_frame_bottom, 
                         height=2,
                         width=13,
                         font="Arial 12",
                         text=f"Start({normal_key_name_2})\nButton 2",
                         #command=active_hotkey             
                         )
button_start_2.pack(side="left", padx=(20, 0))

#bottom bottom frame
#----------------------------------------------
bottom_frame_bottom = tk.Frame(bottom_frame, height=50, width=490, bg="lightgrey")
bottom_frame_bottom.pack(expand=True)
bottom_frame_bottom.pack_propagate(False)

button_theme = tk.Button(bottom_frame_bottom,
                         height=2,
                         width=13,
                         font="Arial 12",
                         text="Theme\nSettings",
                         command=theme_settings
                         )
button_theme.pack(side="left", padx=(110, 0))

button_settings = tk.Button(bottom_frame_bottom,
                             height=2,
                             width=13,
                             font="Arial 12",
                             text="Hotkey\nSettings",
                             command=open_settings
                            )
button_settings.pack(side="left", padx=(20, 0))


#Hotkey settings window
#===================================================
setting_window = tk.Toplevel(root)
setting_window.config(bg="white")
setting_window.title("Hotkey settings")
setting_window.geometry("300x260")
setting_window.resizable(False, False)
setting_window.attributes("-topmost", True)
setting_window.iconbitmap("icons/icon_2.ico")
setting_window.withdraw()
setting_window.protocol("WM_DELETE_WINDOW", close_setting_no_changes)

indent_frame = tk.Frame(setting_window, bg="white", height=10)
indent_frame.pack(side="top")

#first_frame
#----------------------------------------------
first_frame = tk.LabelFrame(setting_window, height=90, width=280, bg="white", font="Arial 10", text="1 mouse setting:")
first_frame.pack(side="top")
first_frame.pack_propagate(False)

button_setting_start = tk.Button(first_frame,
                         font="Arial 14",
                         height=2,
                         width=9,
                         text="Start/Stop",
                         command=hotkey_choice_1
                         )
button_setting_start.pack(side="left", padx=(25, 0))

label_choice = tk.Label(first_frame,
                         font="Arial 14",
                         height=2,
                         width=9,
                         text=normal_key_name_1,
                         relief="ridge"
                         )
label_choice.pack(side="right", padx=(0, 25))

indent_frame_2 = tk.Frame(setting_window, bg="white", height=5)
indent_frame_2.pack(side="top")

#second_frame
#----------------------------------------------
second_frame = tk.LabelFrame(setting_window, height=90, width=280, bg="white", font="Arial 10", text="2 mouse setting")
second_frame.pack(side="top")
second_frame.pack_propagate(False)

button_setting_start_2 = tk.Button(second_frame,
                         font="Arial 14",
                         height=2,
                         width=9,
                         text="Start/Stop",
                         command=hotkey_choice_2
                         )
button_setting_start_2.pack(side="left", padx=(25, 0))

label_choice_2 = tk.Label(second_frame,
                         font="Arial 14",
                         height=2,
                         width=9,
                         text=normal_key_name_2,
                         relief="ridge"
                         )
label_choice_2.pack(side="right", padx=(0, 25))

#third_frame
#----------------------------------------------
third_frame = tk.Frame(setting_window, height=80, width=300, bg="white")
third_frame.pack(side="top")
third_frame.pack_propagate(False)

button_ok = tk.Button(third_frame,
                     font="Arial 14", 
                     height=1,
                     width=6,
                     text="Ok",
                     command=close_settings
                    )
button_ok.pack(side="left", padx=(50, 0))

button_cancel = tk.Button(third_frame,
                         font="Arial 14", 
                         height=1,
                         width=6,
                         text="Cancel",
                         command=close_setting_no_changes
                        )
button_cancel.pack(side="right", padx=(0, 50))

#Основное включение программы:
winmm.timeBeginPeriod(1) 

click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

keyboard_listener = KeyboardListener(on_press=on_press_keyboard)
keyboard_listener.start()

load_settings()
root.mainloop()
winmm.timeEndPeriod(1) 
