import tkinter as tk
from tkinter import scrolledtext
import psutil
import platform
import threading


class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Системный монитор")
        self.root.geometry("600x400")

        tk.Label(root, text="СИСТЕМНЫЙ МОНИТОР", font=("Arial", 14, "bold")).pack(
            pady=10
        )

        tk.Label(root, text=f"ОС: {platform.system()} {platform.release()}").pack()

        self.check_btn = tk.Button(
            root,
            text="ПОКАЗАТЬ ИНФОРМАЦИЮ",
            bg="lightblue",
            font=("Arial", 11, "bold"),
            command=self.start_monitor,
        )
        self.check_btn.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(root, height=15)
        self.result_text.pack(fill="both", padx=10, pady=5, expand=True)

        self.status = tk.Label(
            root, text="Готов к работе", bd=1, relief="sunken", anchor="w"
        )
        self.status.pack(fill="x", padx=10, pady=2)

    def start_monitor(self):
        self.result_text.delete(1.0, tk.END)
        self.check_btn.config(state="disabled")
        self.status.config(text="Сбор информации...")

        thread = threading.Thread(target=self.get_system_info)
        thread.daemon = True
        thread.start()

    def get_system_info(self):
        self.root.after(0, self.add_result, "1. ЗАГРУЗКА CPU:")

        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()

        self.root.after(0, self.add_result, f"   Процессоров: {cpu_count}")
        self.root.after(0, self.add_result, f"   Загрузка: {cpu_percent}%")

        cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
        for i, core in enumerate(cpu_percent_per_core):
            self.root.after(0, self.add_result, f"   Ядро {i+1}: {core}%")

        self.root.after(0, self.add_result, "")
        self.root.after(0, self.add_result, "2. ОПЕРАТИВНАЯ ПАМЯТЬ:")

        memory = psutil.virtual_memory()
        self.root.after(
            0, self.add_result, f"   Всего: {memory.total / (1024**3):.2f} ГБ"
        )
        self.root.after(
            0, self.add_result, f"   Использовано: {memory.used / (1024**3):.2f} ГБ"
        )
        self.root.after(
            0, self.add_result, f"   Свободно: {memory.available / (1024**3):.2f} ГБ"
        )
        self.root.after(0, self.add_result, f"   Загруженность: {memory.percent}%")

        self.root.after(0, self.add_result, "")
        self.root.after(0, self.add_result, "3. ЗАГРУЖЕННОСТЬ ДИСКА:")

        disk = psutil.disk_usage("/")
        self.root.after(
            0, self.add_result, f"   Всего: {disk.total / (1024**3):.2f} ГБ"
        )
        self.root.after(
            0, self.add_result, f"   Использовано: {disk.used / (1024**3):.2f} ГБ"
        )
        self.root.after(
            0, self.add_result, f"   Свободно: {disk.free / (1024**3):.2f} ГБ"
        )
        self.root.after(0, self.add_result, f"   Загруженность: {disk.percent}%")

        self.root.after(0, self.monitor_finished)

    def add_result(self, text):
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)

    def monitor_finished(self):
        self.status.config(text="Информация собрана")
        self.check_btn.config(state="normal")


def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
