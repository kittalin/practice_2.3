import tkinter as tk
from tkinter import scrolledtext
import requests
import threading


class SiteCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Проверка сайтов")
        self.root.geometry("650x450")

        tk.Label(
            root, text="ПРОВЕРКА ДОСТУПНОСТИ САЙТОВ", font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.urls = [
            "https://github.com/",
            "https://www.binance.com/en",
            "https://tomtit.tomsk.ru/",
            "https://jsonplaceholder.typicode.com/",
            "https://moodle.tomtit-tomsk.ru/",
        ]

        tk.Label(root, text="Проверяемые сайты:").pack()

        list_frame = tk.Frame(root)
        list_frame.pack(fill="both", padx=20, pady=5, expand=True)

        for url in self.urls:
            tk.Label(list_frame, text=url, anchor="w").pack(fill="x", pady=1)

        self.check_btn = tk.Button(
            root,
            text="ПРОВЕРИТЬ САЙТЫ",
            bg="lightblue",
            font=("Arial", 11, "bold"),
            command=self.start_check,
        )
        self.check_btn.pack(pady=10)

        tk.Label(root, text="Результаты:").pack()
        self.result_text = scrolledtext.ScrolledText(root, height=10)
        self.result_text.pack(fill="both", padx=20, pady=5, expand=True)

        self.status = tk.Label(
            root, text="Готов к работе", bd=1, relief="sunken", anchor="w"
        )
        self.status.pack(fill="x", padx=20, pady=2)

    def start_check(self):
        self.result_text.delete(1.0, tk.END)
        self.check_btn.config(state="disabled")
        self.status.config(text="Проверка...")

        thread = threading.Thread(target=self.check_sites)
        thread.daemon = True
        thread.start()

    def check_sites(self):
        for url in self.urls:
            self.root.after(0, self.update_status, f"Проверяю: {url}")

            try:
                response = requests.get(url, timeout=5)
                code = response.status_code

                if code == 200:
                    status = "доступен"
                elif code == 403:
                    status = "вход запрещен"
                elif code == 404:
                    status = "не найден"
                elif code >= 500:
                    status = "ошибка сервера"
                else:
                    status = f"код {code}"

                self.root.after(0, self.add_result, f"{url} – {status} – {code}")

            except requests.exceptions.ConnectionError:
                self.root.after(
                    0, self.add_result, f"{url} – не доступен – нет соединения"
                )
            except requests.exceptions.Timeout:
                self.root.after(0, self.add_result, f"{url} – не доступен – таймаут")
            except Exception as e:
                self.root.after(0, self.add_result, f"{url} – ошибка – {str(e)}")

        self.root.after(0, self.check_finished)

    def update_status(self, message):
        self.status.config(text=message)

    def add_result(self, text):
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)

    def check_finished(self):
        self.status.config(text="Проверка завершена")
        self.check_btn.config(state="normal")


def main():
    root = tk.Tk()
    app = SiteCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
