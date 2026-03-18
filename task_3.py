from tkinter import *
from tkinter import scrolledtext, messagebox
import requests
import json
import os

if not os.path.exists("resource"):
    os.makedirs("resource")

save_file = "resource/save.json"
url = "https://www.cbr-xml-daily.ru/daily_json.js"
data = None
groups = {}

try:
    with open(save_file, "r", encoding="utf-8") as f:
        groups = json.load(f)
except:
    groups = {}

root = Tk()
root.title("Курсы валют")
root.geometry("650x550")

Label(root, text="КУРСЫ ВАЛЮТ", font=("Arial", 16, "bold")).pack(pady=10)

try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        data = response.json()["Valute"]
        status_text = "Данные загружены"
    else:
        status_text = "Ошибка загрузки"
except:
    status_text = "Ошибка соединения"


def show_all():
    if not data:
        status.config(text="Данные не загружены")
        return

    result_text.delete(1.0, END)
    result_text.insert(END, "ВСЕ ВАЛЮТЫ:\n")
    result_text.insert(END, "-" * 60 + "\n")

    count = 0
    for code, info in data.items():
        result_text.insert(
            END,
            f"{code} – {info['Name']} – {info['Value']} руб. за {info['Nominal']}\n",
        )
        count += 1
        if count >= 20:
            result_text.insert(END, f"... и еще {len(data) - 20} валют\n")
            break

    result_text.insert(END, f"Всего: {len(data)} валют\n")
    result_text.see(END)


def search_dialog():
    dialog = Toplevel(root)
    dialog.title("Поиск валюты")
    dialog.geometry("250x100")

    Label(dialog, text="Код валюты (USD, EUR):").pack(pady=5)
    entry = Entry(dialog)
    entry.pack(pady=5)

    def search():
        code = entry.get().upper().strip()
        dialog.destroy()

        if not data:
            status.config(text="Данные не загружены")
            return

        result_text.delete(1.0, END)

        if code in data:
            info = data[code]
            result_text.insert(END, f"{code} – {info['Name']}\n")
            result_text.insert(END, "-" * 40 + "\n")
            result_text.insert(
                END, f"Курс: {info['Value']} руб. за {info['Nominal']}\n"
            )
            result_text.insert(END, f"Предыдущий курс: {info['Previous']} руб.\n")
        else:
            result_text.insert(END, f"Валюта {code} не найдена\n")

    Button(dialog, text="Найти", command=search).pack()


def create_group():
    dialog = Toplevel(root)
    dialog.title("Создать группу")
    dialog.geometry("250x120")

    Label(dialog, text="Название группы:").pack(pady=5)
    entry = Entry(dialog)
    entry.pack(pady=5)

    def create():
        name = entry.get().strip()
        if name:
            if name not in groups:
                groups[name] = []
                with open(save_file, "w", encoding="utf-8") as f:
                    json.dump(groups, f, ensure_ascii=False, indent=4)
                status.config(text=f"Группа '{name}' создана")
            else:
                status.config(text=f"Группа '{name}' уже есть")
        dialog.destroy()

    Button(dialog, text="Создать", command=create).pack()


def show_groups():
    result_text.delete(1.0, END)

    if not groups:
        result_text.insert(END, "У вас нет групп\n")
        return

    result_text.insert(END, "ВАШИ ГРУППЫ:\n")
    result_text.insert(END, "-" * 40 + "\n")

    for name, currencies in groups.items():
        if currencies:
            result_text.insert(END, f"{name}: {', '.join(currencies)}\n")
        else:
            result_text.insert(END, f"{name}: пусто\n")

    result_text.see(END)


def add_to_group():
    if not groups:
        messagebox.showinfo("Информация", "Сначала создайте группу")
        return

    dialog = Toplevel(root)
    dialog.title("Добавить в группу")
    dialog.geometry("250x150")

    Label(dialog, text="Группа:").pack()
    group_var = StringVar()
    group_menu = OptionMenu(dialog, group_var, *groups.keys())
    group_menu.pack()

    Label(dialog, text="Код валюты:").pack()
    entry = Entry(dialog)
    entry.pack()

    def add():
        group = group_var.get()
        code = entry.get().upper().strip()

        if not group or not code:
            return

        if code not in data:
            status.config(text=f"Валюта {code} не найдена")
            dialog.destroy()
            return

        if code in groups[group]:
            status.config(text=f"Валюта {code} уже в группе")
        else:
            groups[group].append(code)
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(groups, f, ensure_ascii=False, indent=4)
            status.config(text=f"Валюта {code} добавлена")

        dialog.destroy()

    Button(dialog, text="Добавить", command=add).pack()


def remove_from_group():
    if not groups:
        messagebox.showinfo("Информация", "У вас нет групп")
        return

    dialog = Toplevel(root)
    dialog.title("Удалить из группы")
    dialog.geometry("250x120")

    Label(dialog, text="Группа:").pack()
    group_var = StringVar()
    group_menu = OptionMenu(dialog, group_var, *groups.keys())
    group_menu.pack()

    def show_remove():
        group = group_var.get()
        if not group:
            return

        if not groups[group]:
            status.config(text=f"В группе {group} нет валют")
            dialog.destroy()
            return

        remove_dialog = Toplevel(dialog)
        remove_dialog.title("Выберите валюту")
        remove_dialog.geometry("200x150")

        Label(remove_dialog, text="Валюта:").pack()
        currency_var = StringVar()
        currency_menu = OptionMenu(remove_dialog, currency_var, *groups[group])
        currency_menu.pack()

        def remove():
            currency = currency_var.get()
            groups[group].remove(currency)
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(groups, f, ensure_ascii=False, indent=4)
            status.config(text=f"Валюта {currency} удалена")
            remove_dialog.destroy()
            dialog.destroy()

        Button(remove_dialog, text="Удалить", command=remove).pack()

    Button(dialog, text="Далее", command=show_remove).pack()


btn_frame = Frame(root)
btn_frame.pack(pady=5)

Button(btn_frame, text="Все валюты", width=15, command=show_all).pack(
    side="left", padx=2
)
Button(btn_frame, text="Найти", width=15, command=search_dialog).pack(
    side="left", padx=2
)
Button(btn_frame, text="Создать группу", width=15, command=create_group).pack(
    side="left", padx=2
)
Button(btn_frame, text="Мои группы", width=15, command=show_groups).pack(
    side="left", padx=2
)
Button(btn_frame, text="Добавить в группу", width=15, command=add_to_group).pack(
    side="left", padx=2
)
Button(btn_frame, text="Удалить из группы", width=15, command=remove_from_group).pack(
    side="left", padx=2
)

Label(root, text="Результаты:").pack()
result_text = scrolledtext.ScrolledText(root, height=15)
result_text.pack(fill="both", padx=10, pady=5, expand=True)

status = Label(root, text=status_text, bd=1, relief="sunken", anchor="w")
status.pack(fill="x", padx=10, pady=2)

root.mainloop()
