from tkinter import *
from tkinter import scrolledtext
import psutil
import platform
import os

if not os.path.exists("resource"):
    os.makedirs("resource")

root = Tk()
root.title("Системный монитор")
root.geometry("600x500")

Label(root, text="СИСТЕМНЫЙ МОНИТОР", font=("Arial", 16, "bold")).pack(pady=10)

info_label = Label(root, text="", font=("Arial", 10))
info_label.pack()

os_info = f"ОС: {platform.system()} {platform.release()}"
cpu_info = f"Процессор: {platform.processor()}"
info_label.config(text=f"{os_info}\n{cpu_info}")

result_text = scrolledtext.ScrolledText(root, height=18)
result_text.pack(fill="both", padx=10, pady=5, expand=True)

status = Label(root, text="Готов", bd=1, relief="sunken", anchor="w")
status.pack(fill="x", padx=10, pady=2)


def get_system_info():
    result_text.delete(1.0, END)
    status.config(text="Сбор информации...")
    root.update()

    result_text.insert(END, "1. ЗАГРУЗКА CPU:\n")

    cpu_count = psutil.cpu_count()
    result_text.insert(END, f"Процессоров (ядер): {cpu_count}\n")

    cpu_percent = psutil.cpu_percent(interval=1)
    result_text.insert(END, f"Общая загрузка: {cpu_percent}%\n")

    per_core = psutil.cpu_percent(interval=1, percpu=True)
    i = 1
    for core in per_core:
        result_text.insert(END, f"Ядро {i}: {core}%\n")
        i += 1
    result_text.insert(END, "\n")

    result_text.insert(END, "2. ОПЕРАТИВНАЯ ПАМЯТЬ:\n")
    memory = psutil.virtual_memory()
    total_gb = memory.total / (1024**3)
    used_gb = memory.used / (1024**3)
    free_gb = memory.available / (1024**3)

    result_text.insert(END, f"Всего: {total_gb:.2f} ГБ\n")
    result_text.insert(END, f"Использовано: {used_gb:.2f} ГБ\n")
    result_text.insert(END, f"Свободно: {free_gb:.2f} ГБ\n")
    result_text.insert(END, f"Загруженность: {memory.percent}%\n\n")

    result_text.insert(END, "3. ЗАГРУЖЕННОСТЬ ДИСКА:\n")
    disk = psutil.disk_usage("/")
    total_disk = disk.total / (1024**3)
    used_disk = disk.used / (1024**3)
    free_disk = disk.free / (1024**3)

    result_text.insert(END, f"Всего: {total_disk:.2f} ГБ\n")
    result_text.insert(END, f"Использовано: {used_disk:.2f} ГБ\n")
    result_text.insert(END, f"Свободно: {free_disk:.2f} ГБ\n")
    result_text.insert(END, f"Загруженность: {disk.percent}%\n")

    result_text.see(END)
    status.config(text="Информация собрана")


Button(
    root,
    text="СОБРАТЬ ИНФОРМАЦИЮ",
    bg="lightblue",
    font=("Arial", 11, "bold"),
    command=get_system_info,
).pack(pady=10)

root.mainloop()
