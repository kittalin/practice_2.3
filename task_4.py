from tkinter import *
from tkinter import scrolledtext, messagebox
import requests
import os

if not os.path.exists("resource"):
    os.makedirs("resource")

base_url = "https://api.github.com"

root = Tk()
root.title("GitHub API")
root.geometry("650x550")

Label(root, text="GITHUB API", font=("Arial", 16, "bold")).pack(pady=10)


def profile_dialog():
    dialog = Toplevel(root)
    dialog.title("Профиль пользователя")
    dialog.geometry("250x100")

    Label(dialog, text="Имя пользователя:").pack(pady=5)
    entry = Entry(dialog)
    entry.pack(pady=5)

    def get_profile():
        username = entry.get().strip()
        if username:
            dialog.destroy()

            result_text.delete(1.0, END)
            status.config(text="Загрузка...")
            root.update()

            try:
                response = requests.get(f"{base_url}/users/{username}", timeout=5)

                if response.status_code == 200:
                    data = response.json()

                    name = data.get("name", "Не указано")
                    html_url = data["html_url"]
                    repos = data["public_repos"]
                    following = data["following"]
                    followers = data["followers"]
                    gists = data["public_gists"]

                    result_text.insert(END, "ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ:\n")
                    result_text.insert(END, "-" * 40 + "\n")
                    result_text.insert(END, f"Имя: {name}\n")
                    result_text.insert(END, f"Ссылка: {html_url}\n")
                    result_text.insert(END, f"Репозитории: {repos}\n")
                    result_text.insert(END, f"Подписки: {following}\n")
                    result_text.insert(END, f"Подписчики: {followers}\n")
                    result_text.insert(END, f"Gists: {gists}\n")

                    status.config(text="Готово")
                elif response.status_code == 404:
                    result_text.insert(END, f"Пользователь {username} не найден\n")
                    status.config(text="Не найден")
                else:
                    result_text.insert(END, f"Ошибка: {response.status_code}\n")
                    status.config(text="Ошибка")

            except requests.exceptions.ConnectionError:
                result_text.insert(END, "Ошибка: нет соединения с GitHub\n")
                status.config(text="Ошибка соединения")
            except:
                result_text.insert(END, "Ошибка\n")
                status.config(text="Ошибка")

    Button(dialog, text="Найти", command=get_profile).pack()


def repos_dialog():
    dialog = Toplevel(root)
    dialog.title("Репозитории пользователя")
    dialog.geometry("250x100")

    Label(dialog, text="Имя пользователя:").pack(pady=5)
    entry = Entry(dialog)
    entry.pack(pady=5)

    def get_repos():
        username = entry.get().strip()
        if username:
            dialog.destroy()

            result_text.delete(1.0, END)
            status.config(text="Загрузка...")
            root.update()

            try:
                response = requests.get(f"{base_url}/users/{username}/repos", timeout=5)

                if response.status_code == 200:
                    repos = response.json()

                    if not repos:
                        result_text.insert(
                            END, f"У пользователя {username} нет репозиториев\n"
                        )
                        status.config(text="Готово")
                        return

                    result_text.insert(END, f"РЕПОЗИТОРИИ {username}:\n")
                    result_text.insert(END, "-" * 70 + "\n")

                    i = 1
                    for repo in repos[:10]:
                        name = repo["name"]
                        html_url = repo["html_url"]
                        watchers = repo.get("watchers_count", 0)
                        language = repo.get("language", "Не указан")
                        private = repo["private"]
                        visibility = "Публичный" if not private else "Приватный"
                        default_branch = repo["default_branch"]

                        result_text.insert(END, f"\n{i}. {name}\n")
                        result_text.insert(END, f"Ссылка: {html_url}\n")
                        result_text.insert(END, f"Просмотры: {watchers}\n")
                        result_text.insert(END, f"Язык: {language}\n")
                        result_text.insert(END, f"Видимость: {visibility}\n")
                        result_text.insert(END, f"Ветка: {default_branch}\n")
                        i += 1

                    if len(repos) > 10:
                        result_text.insert(
                            END, f"\n... и еще {len(repos) - 10} репозиториев\n"
                        )

                    status.config(text="Готово")
                elif response.status_code == 404:
                    result_text.insert(END, f"Пользователь {username} не найден\n")
                    status.config(text="Не найден")
                else:
                    result_text.insert(END, f"Ошибка: {response.status_code}\n")
                    status.config(text="Ошибка")

            except requests.exceptions.ConnectionError:
                result_text.insert(END, "Ошибка: нет соединения с GitHub\n")
                status.config(text="Ошибка соединения")
            except:
                result_text.insert(END, "Ошибка\n")
                status.config(text="Ошибка")

    Button(dialog, text="Найти", command=get_repos).pack()


def search_dialog():
    dialog = Toplevel(root)
    dialog.title("Поиск репозиториев")
    dialog.geometry("250x100")

    Label(dialog, text="Название для поиска:").pack(pady=5)
    entry = Entry(dialog)
    entry.pack(pady=5)

    def search():
        query = entry.get().strip()
        if query:
            dialog.destroy()

            result_text.delete(1.0, END)
            status.config(text="Поиск...")
            root.update()

            try:
                response = requests.get(
                    f"{base_url}/search/repositories?q={query}", timeout=5
                )

                if response.status_code == 200:
                    data = response.json()
                    total = data["total_count"]

                    if total == 0:
                        result_text.insert(
                            END, f"Репозитории по запросу '{query}' не найдены\n"
                        )
                        status.config(text="Готово")
                        return

                    result_text.insert(END, f"РЕЗУЛЬТАТЫ ПОИСКА: {query}\n")
                    result_text.insert(END, f"Найдено: {total} репозиториев\n")
                    result_text.insert(END, "-" * 70 + "\n")

                    i = 1
                    for repo in data["items"][:10]:
                        name = repo["name"]
                        owner = repo["owner"]["login"]
                        html_url = repo["html_url"]
                        description = repo.get("description", "Нет описания")
                        language = repo.get("language", "Не указан")
                        stars = repo["stargazers_count"]

                        result_text.insert(END, f"\n{i}. {name}\n")
                        result_text.insert(END, f"Владелец: {owner}\n")
                        result_text.insert(END, f"Ссылка: {html_url}\n")
                        if len(description) > 100:
                            result_text.insert(
                                END, f"Описание: {description[:100]}...\n"
                            )
                        else:
                            result_text.insert(END, f"Описание: {description}\n")
                        result_text.insert(END, f"Язык: {language}\n")
                        result_text.insert(END, f"Звезды: {stars}\n")
                        i += 1

                    if total > 10:
                        result_text.insert(
                            END, f"\n... и еще {total - 10} репозиториев\n"
                        )

                    status.config(text="Готово")
                else:
                    result_text.insert(END, f"Ошибка: {response.status_code}\n")
                    status.config(text="Ошибка")

            except requests.exceptions.ConnectionError:
                result_text.insert(END, "Ошибка: нет соединения с GitHub\n")
                status.config(text="Ошибка соединения")
            except:
                result_text.insert(END, "Ошибка\n")
                status.config(text="Ошибка")

    Button(dialog, text="Найти", command=search).pack()


btn_frame = Frame(root)
btn_frame.pack(pady=5)

Button(btn_frame, text="Профиль", width=12, command=profile_dialog).pack(
    side="left", padx=2
)
Button(btn_frame, text="Репозитории", width=12, command=repos_dialog).pack(
    side="left", padx=2
)
Button(btn_frame, text="Поиск", width=12, command=search_dialog).pack(
    side="left", padx=2
)

Label(root, text="Результаты:").pack()
result_text = scrolledtext.ScrolledText(root, height=20)
result_text.pack(fill="both", padx=10, pady=5, expand=True)

status = Label(root, text="Готов", bd=1, relief="sunken", anchor="w")
status.pack(fill="x", padx=10, pady=2)

root.mainloop()
