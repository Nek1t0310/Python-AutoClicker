import os
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

ACTIVATE_KEY = Key.f8
CHANGED_ACTIVATE_KEY = Key.f8
SETTING_FILE = "settings.json"

normal_key_name = str(ACTIVATE_KEY).replace("Key.", "").replace("'", "").upper()

mouse = Controller()
clicking = False
stop_click = False
is_setting_hotkey = False
random_activate = False
on_press_change = False
click_event = threading.Event()
winmm = ctypes.windll.winmm

SELECTED_BUTTON = Button.left
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

def on_click_setup(event):
    global SELECTED_BUTTON, BUTTON_MAP

    user_choice = mouse_choice_label.get()
    SELECTED_BUTTON = BUTTON_MAP[user_choice]
    #print(f"Кнопка мыши изменена на: {user_choice}")

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
    while not stop_click:
        if clicking:
            mouse.press(SELECTED_BUTTON)
            mouse.release(SELECTED_BUTTON)

            current_delay = CLICK_DELAY

            if random_activate:
                offset_delay = RANDOM_OFFSET_VALUE / 1000
                current_delay += random.uniform(-offset_delay, offset_delay)

                if current_delay < 0.001:
                    current_delay = 0.001

            click_event.wait(timeout=current_delay)
        else:
            time.sleep(0.1)

def hotkey_choice():
    global on_press_change

    on_press_change = True
    label_choice.config(text="Choose key")

def open_settings():
    global is_setting_hotkey

    setting_window.deiconify()
    setting_window.grab_set()
    setting_window.focus_set()
    is_setting_hotkey = True

def close_settings():
    global is_setting_hotkey
    global normal_key_name
    global on_press_change
    global ACTIVATE_KEY
    global CHANGED_ACTIVATE_KEY

    setting_window.grab_release()
    setting_window.withdraw()
    ACTIVATE_KEY = CHANGED_ACTIVATE_KEY
    normal_key_name = str(ACTIVATE_KEY).replace("Key.", "").replace("'", "").upper()
    button_start.config(text=f"Start({normal_key_name})")
    is_setting_hotkey = False
    on_press_change = False

def close_setting_no_changes():
    global is_setting_hotkey
    global on_press_change

    on_press_change = False
    setting_window.grab_release()
    setting_window.withdraw()
    clean_key_name = str(ACTIVATE_KEY).replace("Key.", "").replace("'", "").upper()
    label_choice.config(text=clean_key_name)
    is_setting_hotkey = False

def on_press_keyboard(key):
    global clicking
    global stop_click
    global is_setting_hotkey
    global CLICK_DELAY
    global ACTIVATE_KEY
    global CHANGED_ACTIVATE_KEY

    if is_setting_hotkey and on_press_change: 
        if key in(Key.shift, Key.shift_r, Key.ctrl, Key.ctrl_l, Key.ctrl_r, Key.alt, Key.alt_l, Key.alt_r):
            return

        key_name = str(key).replace("Key.", "").replace("'", "").upper()
        label_choice.config(text=key_name)
        CHANGED_ACTIVATE_KEY = key
        return

    if key == ACTIVATE_KEY and is_setting_hotkey == False:
        if not clicking:
            CLICK_DELAY = click_delay()
            clicking = True
        else:
            clicking = False

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

def save_settings():
    global ACTIVATE_KEY

    if hasattr(ACTIVATE_KEY, 'name') and ACTIVATE_KEY.name is not None:
        key_to_save = ACTIVATE_KEY.name
    else:
        key_to_save = getattr(ACTIVATE_KEY, 'char', 'f8')

    save_data = {
        "min": min_entry.get(),
        "sec": sec_entry.get(),
        "millisec": millisec_entry.get(),
        "activate_random": random_activate,
        "random_offset": offset_choice_label.get(),
        "selected_button": mouse_choice_label.get(),
        "selected_hotkey": key_to_save
    }

    with open(SETTING_FILE, "w", encoding="utf-8") as file:
        json.dump(save_data, file, indent=4, ensure_ascii=False)

    #print("Данные сохранены.")
    root.destroy()

def load_settings():
    global random_activate
    global normal_key_name
    global ACTIVATE_KEY
    global CHANGED_ACTIVATE_KEY

    try:
        with open(SETTING_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        key_name = data.get("selected_hotkey", "f8")

        if key_name in Key.__members__:
            loaded_key = Key[key_name]
        else:
            loaded_key = KeyCode.from_char(key_name.lower())

        ACTIVATE_KEY = loaded_key
        CHANGED_ACTIVATE_KEY = loaded_key
        normal_key_name = str(ACTIVATE_KEY).replace("Key.", "").replace("'", "").upper()
        button_start.config(text=f"Start({normal_key_name})")
        label_choice.config(text=normal_key_name)

        min_entry.delete(0, tk.END)
        min_entry.insert(0, data.get("min", "0"))

        sec_entry.delete(0, tk.END)
        sec_entry.insert(0, data.get("sec", "0"))

        millisec_entry.delete(0, tk.END)
        millisec_entry.insert(0, data.get("millisec", "40"))

        offset_choice_label.delete(0, tk.END)
        offset_choice_label.insert(0, data.get("random_offset", "20"))

        saved_button = data.get("selected_button", "Left")
        mouse_choice_label.set(saved_button)

        random_activate = data.get("activate_random", False)
        if random_activate == True:
            random_offset.set(1)
        else:
            random_offset.set(0)

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
#===================================================
top_frame = tk.LabelFrame(main_frame,
                     font="Arial 10",
                     text="Click interval",
                     height=120,
                     width=490,
                     bg="lightgrey"
                     )
top_frame.pack(expand=True, pady=(5, 5), padx=5)
top_frame.pack_propagate(False)

min_entry = tk.Entry(top_frame,
                     relief="solid",
                     width=7,
                     validate="key",
                     validatecommand=(vcmd, "%P")
                     )
min_entry.insert(0, "0")
min_entry.pack(side="left", padx=(30, 0))

min_time = tk.Label(top_frame,
                    font="Arial 14",
                    text="min",
                    bg="lightgrey"
                    )
min_time.pack(side="left", padx=(5, 10))


sec_entry = tk.Entry(top_frame,
                     relief="solid",
                     width=7,
                     validate="key",
                     validatecommand=(vcmd, "%P")
                     )
sec_entry.insert(0, "0")
sec_entry.pack(side="left", padx=(40, 0))

sec_time = tk.Label(top_frame,
                     font="Arial 14",
                     text="sec",
                     bg="lightgrey"
                    )
sec_time.pack(side="left", padx=(5, 10))


millisec_entry = tk.Entry(top_frame,
                         relief="solid",
                         width=7,
                         validate="key",
                         validatecommand=(vcmd, "%P")
                         )
millisec_entry.insert(0, "40")
millisec_entry.pack(side="left", padx=(40, 0))

millisec_time = tk.Label(top_frame,
                         font="Arial 14",
                         text="milliseconds",
                         bg="lightgrey"
                         )
millisec_time.pack(side="left", padx=(5, 10))

#middle frame
#===================================================
middle_frame = tk.LabelFrame(main_frame,
                         font="Arial 10",
                         text="Click options",
                         height=120,
                         width=490, 
                         bg="lightgrey"
                        )
middle_frame.pack(expand=True, padx=5)
middle_frame.pack_propagate(False)

top_middle_frame = tk.Frame(middle_frame,
                             height=40,
                             width=600,
                             bg="lightgrey"
                            )
top_middle_frame.pack(side="top")
top_middle_frame.pack_propagate(False)

mouse_choice = tk.Label(top_middle_frame,
                         font="Arial 14",
                         text="Mouse Button:",
                         bg="lightgrey"
                        )
mouse_choice.pack(side="left", padx=(130, 0))

mouse_choice_label = ttk.Combobox(top_middle_frame,
                             font="Arial 14",
                             values=["Left", "Right", "Middle"],
                             width=8,
                             state="readonly"
                            )
mouse_choice_label.set("Left")
mouse_choice_label.pack(side="left", padx=(10, 0))
mouse_choice_label.bind("<<ComboboxSelected>>", on_click_setup)

#----------------------------------------------

bottom_middle_frame = tk.Frame(middle_frame,
                             height=60,
                             width=600,
                             bg="lightgrey"
                            )
bottom_middle_frame.pack(side="top")
bottom_middle_frame.pack_propagate(False)

offset_button_information = tk.Button(bottom_middle_frame,
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
offset_button = tk.Checkbutton(bottom_middle_frame,
                         text="Random Offset +-",
                         font="Arial 14",
                         relief="flat",
                         bg="lightgrey",
                         variable=random_offset,
                         command=switch_random
                        )
offset_button.pack(side="left", padx=(5, 0))

offset_choice_label = tk.Entry(bottom_middle_frame,
                             font="Arial 14",
                             relief="sunken",
                             width=3,
                             validate="key",
                             validatecommand=(vcmd_2, "%P")
                            )
offset_choice_label.insert(0, "20")
offset_choice_label.pack(side="left", padx=(10, 0))

offset_time = tk.Label(bottom_middle_frame,
                         font="Arial 14",
                         text="milliseconds",
                         bg="lightgrey"
                       )
offset_time.pack(side="left", padx=(5, 0))

#bottom frame
#===================================================
bottom_frame = tk.LabelFrame(main_frame,
                         font="Arial 10",
                         text="Settings",
                         height=150,
                         width=490,
                         bg="lightgrey",
                        )
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
                         text=f"Start({normal_key_name})",
                         )
button_start.pack(side="left", padx=(110, 0))

button_settings = tk.Button(top_frame_bottom,
                             height=2,
                             width=13,
                             font="Arial 12",
                             text="Hotkey\nSettings",
                             command=open_settings
                            )
button_settings.pack(side="left", padx=(20, 0))

#----------------------------------------------

bottom_frame_bottom = tk.Frame(bottom_frame,
                                 height=50,
                                 width=490,
                                 bg="lightgrey"
                               )
bottom_frame_bottom.pack(expand=True)
bottom_frame_bottom.pack_propagate(False)

button_theme = tk.Button(bottom_frame_bottom,
                         height=2,
                         width=13,
                         font="Arial 12",
                         text="Theme\nSettings",
                         command=theme_settings
                         )
button_theme.pack(expand=True)

setting_window = tk.Toplevel(root)
setting_window.config(bg="white")
setting_window.title("Hotkey settings")
setting_window.geometry("300x180")
setting_window.resizable(False, False)
setting_window.attributes("-topmost", True)
setting_window.iconbitmap("icons/icon_2.ico")
setting_window.withdraw()
setting_window.protocol("WM_DELETE_WINDOW", close_setting_no_changes)

indent_frame = tk.Frame(setting_window, height=10, width=300, bg="white")
indent_frame.pack(side="top")

first_frame = tk.Frame(setting_window,
                     height=80,
                     width=300,
                     bg="white"
                     )
first_frame.pack(side="top")
first_frame.pack_propagate(False)

button_setting_start = tk.Button(first_frame,
                         font="Arial 14",
                         height=2,
                         width=9,
                         text="Start/Stop",
                         command=hotkey_choice
                         )
button_setting_start.pack(side="left", padx=(35, 0))

label_choice = tk.Label(first_frame,
                         font="Arial 14",
                         height=2,
                         width=9,
                         text=normal_key_name,
                         relief="ridge"
                         )
label_choice.pack(side="right", padx=(0, 35))

#----------------------------------------------

second_frame = tk.Frame(setting_window,
                     height=80,
                     width=300,
                     bg="white"   
                     )
second_frame.pack(side="top")
second_frame.pack_propagate(False)

button_ok = tk.Button(second_frame,
                     font="Arial 14", 
                     height=1,
                     width=6,
                     text="Ok",
                     command=close_settings
                    )
button_ok.pack(side="left", padx=(50, 0))

button_cancel = tk.Button(second_frame,
                         font="Arial 14", 
                         height=1,
                         width=6,
                         text="Cancel",
                         command=close_setting_no_changes
                        )
button_cancel.pack(side="right", padx=(0, 50))

winmm.timeBeginPeriod(1) 

click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

keyboard_listener = KeyboardListener(on_press=on_press_keyboard)
keyboard_listener.start()

load_settings()
root.mainloop()
winmm.timeEndPeriod(1) 
