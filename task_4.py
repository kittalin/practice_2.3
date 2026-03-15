import tkinter as tk
from tkinter import scrolledtext
import requests
import threading


class GitHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub API")
        self.root.geometry("600x500")

        self.base_url = "https://api.github.com"

        tk.Label(root, text="GITHUB API", font=("Arial", 14, "bold")).pack(pady=5)

        tk.Label(root, text="Выберите действие:").pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame,
            text="1. Профиль пользователя",
            width=25,
            command=self.profile_dialog,
        ).pack(pady=2)
        tk.Button(
            btn_frame,
            text="2. Репозитории пользователя",
            width=25,
            command=self.repos_dialog,
        ).pack(pady=2)
        tk.Button(
            btn_frame,
            text="3. Поиск репозиториев",
            width=25,
            command=self.search_dialog,
        ).pack(pady=2)

        tk.Label(root, text="Результаты:").pack()
        self.result_text = scrolledtext.ScrolledText(root, height=18)
        self.result_text.pack(fill="both", padx=10, pady=5, expand=True)

        self.status = tk.Label(
            root, text="Готов к работе", bd=1, relief="sunken", anchor="w"
        )
        self.status.pack(fill="x", padx=10, pady=2)

    def profile_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Профиль пользователя")
        dialog.geometry("250x100")

        tk.Label(dialog, text="Введите имя пользователя:").pack(pady=5)
        self.profile_entry = tk.Entry(dialog)
        self.profile_entry.pack(pady=5)

        def get_profile():
            username = self.profile_entry.get().strip()
            if username:
                dialog.destroy()
                self.get_user_profile(username)

        tk.Button(dialog, text="Найти", command=get_profile).pack()

    def get_user_profile(self, username):
        self.result_text.delete(1.0, tk.END)
        self.status.config(text="Загрузка...")

        def fetch():
            try:
                response = requests.get(f"{self.base_url}/users/{username}", timeout=5)

                if response.status_code == 200:
                    data = response.json()

                    name = data.get("name", "Не указано")
                    html_url = data["html_url"]
                    public_repos = data["public_repos"]
                    following = data["following"]
                    followers = data["followers"]
                    public_gists = data["public_gists"]

                    self.root.after(
                        0,
                        self.display_profile,
                        name,
                        html_url,
                        public_repos,
                        following,
                        followers,
                        public_gists,
                    )

                elif response.status_code == 404:
                    self.root.after(
                        0, self.show_result, f"Пользователь {username} не найден"
                    )
                else:
                    self.root.after(
                        0, self.show_result, f"Ошибка: {response.status_code}"
                    )

            except Exception as e:
                self.root.after(0, self.show_result, f"Ошибка: {str(e)}")

        thread = threading.Thread(target=fetch)
        thread.daemon = True
        thread.start()

    def display_profile(self, name, url, repos, following, followers, gists):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ:\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        self.result_text.insert(tk.END, f"Имя: {name}\n")
        self.result_text.insert(tk.END, f"Ссылка на профиль: {url}\n")
        self.result_text.insert(tk.END, f"Количество репозиториев: {repos}\n")
        self.result_text.insert(tk.END, f"Количество обсуждений (gists): {gists}\n")
        self.result_text.insert(tk.END, f"Количество подписок: {following}\n")
        self.result_text.insert(tk.END, f"Количество подписчиков: {followers}\n")
        self.status.config(text="Готово")

    def repos_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Репозитории пользователя")
        dialog.geometry("250x100")

        tk.Label(dialog, text="Введите имя пользователя:").pack(pady=5)
        self.repos_entry = tk.Entry(dialog)
        self.repos_entry.pack(pady=5)

        def get_repos():
            username = self.repos_entry.get().strip()
            if username:
                dialog.destroy()
                self.get_user_repos(username)

        tk.Button(dialog, text="Найти", command=get_repos).pack()

    def get_user_repos(self, username):
        self.result_text.delete(1.0, tk.END)
        self.status.config(text="Загрузка...")

        def fetch():
            try:
                response = requests.get(
                    f"{self.base_url}/users/{username}/repos", timeout=5
                )

                if response.status_code == 200:
                    repos = response.json()

                    if not repos:
                        self.root.after(
                            0,
                            self.show_result,
                            f"У пользователя {username} нет репозиториев",
                        )
                        return

                    self.root.after(0, self.display_repos, repos)

                elif response.status_code == 404:
                    self.root.after(
                        0, self.show_result, f"Пользователь {username} не найден"
                    )
                else:
                    self.root.after(
                        0, self.show_result, f"Ошибка: {response.status_code}"
                    )

            except Exception as e:
                self.root.after(0, self.show_result, f"Ошибка: {str(e)}")

        thread = threading.Thread(target=fetch)
        thread.daemon = True
        thread.start()

    def display_repos(self, repos):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"РЕПОЗИТОРИИ ПОЛЬЗОВАТЕЛЯ:\n")
        self.result_text.insert(tk.END, "-" * 70 + "\n")

        for repo in repos[:10]:
            name = repo["name"]
            html_url = repo["html_url"]
            watchers = repo.get("watchers_count", 0)
            language = repo.get("language", "Не указан")
            private = repo["private"]
            visibility = "Публичный" if not private else "Приватный"
            default_branch = repo["default_branch"]

            self.result_text.insert(tk.END, f"\nНазвание: {name}\n")
            self.result_text.insert(tk.END, f"Ссылка на репозиторий: {html_url}\n")
            self.result_text.insert(tk.END, f"Количество просмотров: {watchers}\n")
            self.result_text.insert(tk.END, f"Используемый язык: {language}\n")
            self.result_text.insert(tk.END, f"Видимость: {visibility}\n")
            self.result_text.insert(tk.END, f"Ветка по умолчанию: {default_branch}\n")
            self.result_text.insert(tk.END, "-" * 40 + "\n")

        self.status.config(text="Готово")

    def search_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Поиск репозиториев")
        dialog.geometry("250x100")

        tk.Label(dialog, text="Введите название для поиска:").pack(pady=5)
        self.search_entry = tk.Entry(dialog)
        self.search_entry.pack(pady=5)

        def search():
            query = self.search_entry.get().strip()
            if query:
                dialog.destroy()
                self.search_repositories(query)

        tk.Button(dialog, text="Найти", command=search).pack()

    def search_repositories(self, query):
        self.result_text.delete(1.0, tk.END)
        self.status.config(text="Поиск...")

        def fetch():
            try:
                response = requests.get(
                    f"{self.base_url}/search/repositories?q={query}", timeout=5
                )

                if response.status_code == 200:
                    data = response.json()
                    total = data["total_count"]

                    if total == 0:
                        self.root.after(
                            0,
                            self.show_result,
                            f"Репозитории по запросу '{query}' не найдены",
                        )
                        return

                    self.root.after(
                        0, self.display_search_results, data["items"][:10], total, query
                    )

                else:
                    self.root.after(
                        0, self.show_result, f"Ошибка: {response.status_code}"
                    )

            except Exception as e:
                self.root.after(0, self.show_result, f"Ошибка: {str(e)}")

        thread = threading.Thread(target=fetch)
        thread.daemon = True
        thread.start()

    def display_search_results(self, items, total, query):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"РЕЗУЛЬТАТЫ ПОИСКА: {query}\n")
        self.result_text.insert(tk.END, f"Найдено: {total} репозиториев\n")
        self.result_text.insert(tk.END, "-" * 70 + "\n")

        for repo in items:
            name = repo["name"]
            owner = repo["owner"]["login"]
            html_url = repo["html_url"]
            description = repo.get("description", "Нет описания")
            language = repo.get("language", "Не указан")
            stars = repo["stargazers_count"]

            self.result_text.insert(tk.END, f"\nНазвание: {name}\n")
            self.result_text.insert(tk.END, f"Владелец: {owner}\n")
            self.result_text.insert(tk.END, f"Ссылка: {html_url}\n")
            self.result_text.insert(tk.END, f"Описание: {description}\n")
            self.result_text.insert(tk.END, f"Язык: {language}\n")
            self.result_text.insert(tk.END, f"Звезды: {stars}\n")
            self.result_text.insert(tk.END, "-" * 40 + "\n")

        self.status.config(text="Готово")

    def show_result(self, message):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message + "\n")
        self.status.config(text="Готово")


def main():
    root = tk.Tk()
    app = GitHubApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
