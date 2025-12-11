import tkinter as tk
from tkinter import messagebox
from database.client_repository import ClientRepository


class ClientWindow:
    def __init__(self, root):
        self.root = root
        self.repo = ClientRepository()

        root.title("Управління клієнтами")
        root.geometry("600x450")

        # Поля введення (ID нема!)
        tk.Label(root, text="Ім'я:").grid(row=0, column=0, pady=5)
        self.entry_name = tk.Entry(root, width=30)
        self.entry_name.grid(row=0, column=1, pady=5)

        tk.Label(root, text="Телефон:").grid(row=1, column=0, pady=5)
        self.entry_phone = tk.Entry(root, width=30)
        self.entry_phone.grid(row=1, column=1, pady=5)

        # Кнопки CRUD
        tk.Button(root, text="Додати", width=20, command=self.add_client).grid(row=2, column=0, pady=5)
        tk.Button(root, text="Оновити", width=20, command=self.update_client).grid(row=2, column=1)
        tk.Button(root, text="Видалити", width=20, command=self.delete_client).grid(row=3, column=0)
        tk.Button(root, text="Оновити список", width=20, command=self.load_clients).grid(row=3, column=1)

        # ======= ТАБЛИЦЯ КЛІЄНТІВ =======
        tk.Label(root, text="Список клієнтів:", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=10)

        self.listbox = tk.Listbox(root, width=80, height=12)
        self.listbox.grid(row=5, column=0, columnspan=2, padx=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.selected_id = None  # Зберігаємо ID обраного клієнта

        self.load_clients()

    # Завантаження клієнтів у таблицю
    def load_clients(self):
        self.listbox.delete(0, tk.END)
        clients = self.repo.get_all_clients()

        for c in clients:
            line = f"ID:{c['clientId']} | {c['clientName']} | {c['clientPhone']}"
            self.listbox.insert(tk.END, line)

    # Вибір клієнта в списку
    def on_select(self, event):
        try:
            index = self.listbox.curselection()[0]
            line = self.listbox.get(index)

            # Парсимо ID
            self.selected_id = int(line.split("|")[0].replace("ID:", "").strip())

            # Парсимо ім'я і телефон
            parts = line.split("|")
            name = parts[1].strip()
            phone = parts[2].strip()

            # Вставляємо дані в поля
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, name)

            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(0, phone)

        except:
            pass

    # CRUD операції
    def add_client(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()

        if not name or not phone:
            messagebox.showerror("Помилка", "Заповніть всі поля")
            return

        self.repo.create_client(name, phone)
        self.load_clients()
        messagebox.showinfo("Успіх", "Клієнта додано")

    def update_client(self):
        if not self.selected_id:
            messagebox.showerror("Помилка", "Оберіть клієнта зі списку")
            return

        name = self.entry_name.get()
        phone = self.entry_phone.get()

        self.repo.update_client(self.selected_id, name, phone)
        self.load_clients()
        messagebox.showinfo("Успіх", "Дані оновлено")

    def delete_client(self):
        if not self.selected_id:
            messagebox.showerror("Помилка", "Оберіть клієнта зі списку")
            return

        self.repo.delete_client(self.selected_id)
        self.load_clients()
        messagebox.showinfo("Успіх", "Клієнта видалено")
