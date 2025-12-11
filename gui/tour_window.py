import tkinter as tk
from tkinter import messagebox
from database.tour_repository import TourRepository


class TourWindow:
    def __init__(self, root):
        self.root = root
        self.repo = TourRepository()

        root.title("Управління турами")
        root.geometry("750x500")

        # Поля (без ID)
        tk.Label(root, text="Назва").grid(row=0, column=0, pady=5)
        self.entry_name = tk.Entry(root, width=40)
        self.entry_name.grid(row=0, column=1, pady=5)

        tk.Label(root, text="Маршрут").grid(row=1, column=0, pady=5)
        self.entry_route = tk.Entry(root, width=40)
        self.entry_route.grid(row=1, column=1, pady=5)

        tk.Label(root, text="Дата початку (YYYY-MM-DD)").grid(row=2, column=0, pady=5)
        self.entry_start = tk.Entry(root, width=40)
        self.entry_start.grid(row=2, column=1, pady=5)

        tk.Label(root, text="Тривалість (днів)").grid(row=3, column=0, pady=5)
        self.entry_duration = tk.Entry(root, width=40)
        self.entry_duration.grid(row=3, column=1, pady=5)

        tk.Label(root, text="Ціна").grid(row=4, column=0, pady=5)
        self.entry_price = tk.Entry(root, width=40)
        self.entry_price.grid(row=4, column=1, pady=5)

        # CRUD кнопки
        tk.Button(root, text="Додати", width=20, command=self.add_tour).grid(row=5, column=0, pady=5)
        tk.Button(root, text="Оновити", width=20, command=self.update_tour).grid(row=5, column=1, pady=5)
        tk.Button(root, text="Видалити", width=20, command=self.delete_tour).grid(row=6, column=0)
        tk.Button(root, text="Показати всі", width=20, command=self.load_tours).grid(row=6, column=1)

        # Таблиця турів
        tk.Label(root, text="Список турів:", font=("Arial", 12, "bold")).grid(
            row=7, column=0, columnspan=2, pady=10
        )

        self.listbox = tk.Listbox(root, width=110, height=12)
        self.listbox.grid(row=8, column=0, columnspan=2, padx=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.selected_id = None
        self.load_tours()

    # Завантаження турів
    def load_tours(self):
        self.listbox.delete(0, tk.END)
        tours = self.repo.get_all_tours()

        for t in tours:
            line = (
                f"ID:{t['tourId']} | {t['tourName']} | {t['route']} | "
                f"{t['startDate']} | {t['duration']} днів | {t['price']} грн"
            )
            self.listbox.insert(tk.END, line)

    # Вибір зі списку
    def on_select(self, event):
        try:
            index = self.listbox.curselection()[0]
            line = self.listbox.get(index)

            parts = [p.strip() for p in line.split("|")]

            self.selected_id = int(parts[0].replace("ID:", "").strip())

            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, parts[1])

            self.entry_route.delete(0, tk.END)
            self.entry_route.insert(0, parts[2])

            self.entry_start.delete(0, tk.END)
            self.entry_start.insert(0, parts[3])

            self.entry_duration.delete(0, tk.END)
            self.entry_duration.insert(0, parts[4].replace("днів", "").strip())

            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, parts[5].replace("грн", "").strip())

        except:
            pass

    # CRUD операції
    def add_tour(self):
        name = self.entry_name.get()
        route = self.entry_route.get()
        start = self.entry_start.get()
        duration = self.entry_duration.get()
        price = self.entry_price.get()

        if not name or not route or not start or not duration or not price:
            messagebox.showerror("Помилка", "Заповніть всі поля")
            return

        self.repo.create_tour(name, route, start, duration, price)
        self.load_tours()
        messagebox.showinfo("Успіх", "Тур додано")

    def update_tour(self):
        if not self.selected_id:
            messagebox.showerror("Помилка", "Оберіть тур зі списку")
            return

        name = self.entry_name.get()
        route = self.entry_route.get()
        start = self.entry_start.get()
        duration = self.entry_duration.get()
        price = self.entry_price.get()

        self.repo.update_tour(self.selected_id, name, route, start, duration, price)
        self.load_tours()
        messagebox.showinfo("Успіх", "Тур оновлено")

    def delete_tour(self):
        if not self.selected_id:
            messagebox.showerror("Помилка", "Оберіть тур зі списку")
            return

        self.repo.delete_tour(self.selected_id)
        self.load_tours()
        messagebox.showinfo("Успіх", "Тур видалено")
