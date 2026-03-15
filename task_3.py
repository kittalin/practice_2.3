import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import os
import threading


class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы валют")
        self.root.geometry("600x500")

        if not os.path.exists("resource"):
            os.makedirs("resource")

        self.save_file = "resource/save.json"
        self.url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.currency_data = None
        self.groups = self.load_groups()

        tk.Label(root, text="КУРСЫ ВАЛЮТ", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(root, text="Выберите действие:").pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame, text="1. Все валюты", width=20, command=self.show_all_currencies
        ).pack(pady=2)
        tk.Button(
            btn_frame, text="2. Поиск по коду", width=20, command=self.search_dialog
        ).pack(pady=2)
        tk.Button(
            btn_frame,
            text="3. Создать группу",
            width=20,
            command=self.create_group_dialog,
        ).pack(pady=2)
        tk.Button(
            btn_frame, text="4. Мои группы", width=20, command=self.show_groups
        ).pack(pady=2)
        tk.Button(
            btn_frame,
            text="5. Добавить в группу",
            width=20,
            command=self.add_to_group_dialog,
        ).pack(pady=2)
        tk.Button(
            btn_frame,
            text="6. Удалить из группы",
            width=20,
            command=self.remove_from_group_dialog,
        ).pack(pady=2)

        tk.Label(root, text="Результаты:").pack()
        self.result_text = scrolledtext.ScrolledText(root, height=15)
        self.result_text.pack(fill="both", padx=10, pady=5, expand=True)

        self.status = tk.Label(
            root, text="Готов к работе", bd=1, relief="sunken", anchor="w"
        )
        self.status.pack(fill="x", padx=10, pady=2)

        self.load_currency_data()

    def load_currency_data(self):
        def load():
            try:
                response = requests.get(self.url, timeout=5)
                if response.status_code == 200:
                    self.currency_data = response.json()["Valute"]
                    self.root.after(0, self.update_status, "Данные загружены")
                else:
                    self.root.after(0, self.update_status, "Ошибка загрузки")
            except Exception as e:
                self.root.after(0, self.update_status, f"Ошибка: {str(e)}")

        thread = threading.Thread(target=load)
        thread.daemon = True
        thread.start()

    def show_all_currencies(self):
        if not self.currency_data:
            self.update_status("Данные еще не загружены")
            return

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "ВСЕ ВАЛЮТЫ:\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")

        for code, info in self.currency_data.items():
            self.result_text.insert(
                tk.END,
                f"{code} – {info['Name']} – {info['Value']} руб. за {info['Nominal']}\n",
            )

    def search_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Поиск валюты")
        dialog.geometry("250x100")

        tk.Label(dialog, text="Введите код (USD, EUR):").pack(pady=5)
        entry = tk.Entry(dialog)
        entry.pack(pady=5)

        def search():
            code = entry.get().upper().strip()
            dialog.destroy()
            self.search_currency(code)

        tk.Button(dialog, text="Найти", command=search).pack()

    def search_currency(self, code):
        if not self.currency_data:
            self.update_status("Данные еще не загружены")
            return

        self.result_text.delete(1.0, tk.END)

        if code in self.currency_data:
            info = self.currency_data[code]
            self.result_text.insert(tk.END, f"НАЙДЕНО:\n")
            self.result_text.insert(tk.END, "-" * 50 + "\n")
            self.result_text.insert(tk.END, f"{code} – {info['Name']}\n")
            self.result_text.insert(
                tk.END, f"Курс: {info['Value']} руб. за {info['Nominal']}\n"
            )
        else:
            self.result_text.insert(tk.END, f"Валюта {code} не найдена\n")

    def load_groups(self):
        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_groups(self):
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(self.groups, f, ensure_ascii=False, indent=4)

    def create_group_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Создать группу")
        dialog.geometry("250x120")

        tk.Label(dialog, text="Название группы:").pack(pady=5)
        entry = tk.Entry(dialog)
        entry.pack(pady=5)

        def create():
            name = entry.get().strip()
            if name:
                if name not in self.groups:
                    self.groups[name] = []
                    self.save_groups()
                    self.update_status(f"Группа '{name}' создана")
                else:
                    self.update_status(f"Группа '{name}' уже есть")
            dialog.destroy()

        tk.Button(dialog, text="Создать", command=create).pack()

    def show_groups(self):
        self.result_text.delete(1.0, tk.END)

        if not self.groups:
            self.result_text.insert(tk.END, "Нет созданных групп\n")
            return

        self.result_text.insert(tk.END, "МОИ ГРУППЫ:\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")

        for name, currencies in self.groups.items():
            if currencies:
                self.result_text.insert(tk.END, f"{name}: {', '.join(currencies)}\n")
            else:
                self.result_text.insert(tk.END, f"{name}: пусто\n")

    def add_to_group_dialog(self):
        if not self.groups:
            self.update_status("Нет групп. Сначала создайте группу")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить в группу")
        dialog.geometry("250x150")

        tk.Label(dialog, text="Группа:").pack()
        group_var = tk.StringVar()
        group_menu = tk.OptionMenu(dialog, group_var, *self.groups.keys())
        group_menu.pack()

        tk.Label(dialog, text="Код валюты:").pack()
        entry = tk.Entry(dialog)
        entry.pack()

        def add():
            group = group_var.get()
            code = entry.get().upper().strip()

            if not group or not code:
                return

            if code not in self.currency_data:
                self.update_status(f"Валюта {code} не найдена")
                dialog.destroy()
                return

            if code in self.groups[group]:
                self.update_status(f"Валюта {code} уже в группе")
            else:
                self.groups[group].append(code)
                self.save_groups()
                self.update_status(f"Валюта {code} добавлена в {group}")

            dialog.destroy()

        tk.Button(dialog, text="Добавить", command=add).pack()

    def remove_from_group_dialog(self):
        if not self.groups:
            self.update_status("Нет групп")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Удалить из группы")
        dialog.geometry("250x120")

        tk.Label(dialog, text="Группа:").pack()
        group_var = tk.StringVar()
        group_menu = tk.OptionMenu(dialog, group_var, *self.groups.keys())
        group_menu.pack()

        def show_remove():
            group = group_var.get()
            if not group or group not in self.groups:
                return

            if not self.groups[group]:
                self.update_status(f"В группе {group} нет валют")
                dialog.destroy()
                return

            remove_dialog = tk.Toplevel(dialog)
            remove_dialog.title("Выберите валюту")
            remove_dialog.geometry("200x150")

            tk.Label(remove_dialog, text="Валюта:").pack()
            currency_var = tk.StringVar()
            currency_menu = tk.OptionMenu(
                remove_dialog, currency_var, *self.groups[group]
            )
            currency_menu.pack()

            def remove():
                currency = currency_var.get()
                self.groups[group].remove(currency)
                self.save_groups()
                self.update_status(f"Валюта {currency} удалена из {group}")
                remove_dialog.destroy()
                dialog.destroy()

            tk.Button(remove_dialog, text="Удалить", command=remove).pack()

        tk.Button(dialog, text="Далее", command=show_remove).pack()

    def update_status(self, message):
        self.status.config(text=message)


def main():
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
