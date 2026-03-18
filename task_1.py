from tkinter import *
from tkinter import scrolledtext
import requests
import os

if not os.path.exists("resource"):
    os.makedirs("resource")

root = Tk()
root.title("Проверка сайтов")
root.geometry("600x500")

Label(root, text="ПРОВЕРКА САЙТОВ", font=("Arial", 16, "bold")).pack(pady=10)

Label(root, text="Список сайтов:").pack()

urls = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/",
]

listbox = Listbox(root, height=5)
listbox.pack(fill="x", padx=20, pady=5)

for url in urls:
    listbox.insert(END, url)

result_text = scrolledtext.ScrolledText(root, height=15)
result_text.pack(fill="both", padx=10, pady=5, expand=True)

status = Label(root, text="Готов", bd=1, relief="sunken", anchor="w")
status.pack(fill="x", padx=10, pady=2)


def check_sites():
    result_text.delete(1.0, END)
    status.config(text="Проверка...")
    root.update()

    urls_list = list(listbox.get(0, END))

    for url in urls_list:
        status.config(text=f"Проверяю: {url}")
        root.update()

        try:
            response = requests.get(url, timeout=5)
            code = response.status_code

            if code == 200:
                text = "доступен"
            elif code == 403:
                text = "вход запрещен"
            elif code == 404:
                text = "не найден"
            elif code >= 500:
                text = "ошибка сервера"
            else:
                text = f"код {code}"

            result_text.insert(END, f"{url} – {text} – {code}\n")

        except requests.exceptions.ConnectionError:
            result_text.insert(END, f"{url} – не доступен – нет соединения\n")
        except requests.exceptions.Timeout:
            result_text.insert(END, f"{url} – не доступен – таймаут\n")
        except:
            result_text.insert(END, f"{url} – ошибка\n")

        result_text.see(END)
        root.update()

    status.config(text="Проверка завершена")


Button(
    root,
    text="ПРОВЕРИТЬ",
    bg="lightblue",
    font=("Arial", 11, "bold"),
    command=check_sites,
).pack(pady=10)

root.mainloop()
