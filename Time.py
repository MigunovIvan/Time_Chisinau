import os
import time
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import pythoncom
import win32com.client
import sys

# Функция для создания ярлыка
def create_shortcut(target, shortcut_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.save()

# Функция для добавления программы в автозагрузку
def add_to_startup():
    user_name = os.getlogin()
    startup_path = f"C:\\Users\\{user_name}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    app_name = "MD_News.py"  # Имя вашего скрипта (или EXE после упаковки)
    shortcut_path = os.path.join(startup_path, f"{app_name}.lnk")

    if not os.path.exists(shortcut_path):
        choice = messagebox.askyesno("Автозагрузка", "Добавить приложение в автозагрузку?")
        if choice:
            try:
                create_shortcut(os.path.abspath(sys.argv[0]), shortcut_path)
                messagebox.showinfo("Успех", "Программа добавлена в автозагрузку")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать ярлык: {e}")
        else:
            messagebox.showinfo("Пропуск", "Программа не будет добавлена в автозагрузку")

# Функция для обновления времени
def update_time():
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d-%m-%Y")

    time_label.configure(text=current_time)
    date_label.configure(text=current_date)

    # Обновление каждую секунду
    root.after(1000, update_time)

# Эффект пульсации
def pulse_effect():
    current_font_size = time_label.cget("font")[1]
    new_size = current_font_size + 2 if current_font_size < 50 else current_font_size - 2
    time_label.configure(font=("Helvetica", new_size))
    root.after(1000, pulse_effect)  # Обновляем эффект каждую секунду

# Эффект моргания для времени
def blink_time():
    current_color = time_label.cget("text_color")
    new_color = "#1E90FF" if current_color == "#E6E6FA" else "#E6E6FA"  # Ярко-синий и светло-фиолетовый
    time_label.configure(text_color=new_color)
    root.after(500, blink_time)  # Обновляем эффект каждые 500 мс

# Эффект затемнения для даты
def fade_effect():
    current_color = date_label.cget("text_color")
    new_color = "#E6E6FA" if current_color == "#FFD700" else "#FFD700"
    date_label.configure(text_color=new_color)
    root.after(500, fade_effect)  # Обновляем эффект каждые 500 мс

# Создание главного окна
root = ctk.CTk()
root.title("Виджет даты и времени")
root.geometry("400x300")

# Установка фонового изображения для главного окна
def resource_path(relative_path):
    """ Получить абсолютный путь к ресурсу, работая как в dev, так и в freeze. """
    try:
        # PyInstaller создаёт временную папку для приложения
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

bg_image = ctk.CTkImage(Image.open(resource_path("dove.png")), size=(400, 300))
bg_label = ctk.CTkLabel(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Настройка стиля для отображения времени
time_label = ctk.CTkLabel(root, text="", font=("Helvetica", 48), text_color="#E6E6FA", fg_color="transparent")  # Светло-фиолетовый
time_label.place(relx=0.5, rely=0.4, anchor="center")  # Опустили вниз

# Создание метки для обводки даты
date_label_outline = ctk.CTkLabel(root, text="", font=("Helvetica", 32), text_color="#E6E6FA", fg_color="transparent")  # Обводка
date_label_outline.place(relx=0.5, rely=0.6, anchor="center")

# Создание метки для даты
date_label = ctk.CTkLabel(root, text="", font=("Helvetica", 32), text_color="#FFD700")  # Золотистый
date_label.place(relx=0.5, rely=0.6, anchor="center")  # Опустили вниз

# Запуск обновления времени
update_time()

# Запуск анимации
pulse_effect()

# Запуск эффекта моргания для времени
blink_time()

# Запуск эффекта затемнения для даты
fade_effect()

# Запуск автозагрузки при первом запуске программы
add_to_startup()

# Запуск главного цикла приложения
root.mainloop()
