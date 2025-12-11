import tkinter as tk
from gui.client_window import ClientWindow
from gui.tour_window import TourWindow

def open_client_window():
    win = tk.Toplevel()
    ClientWindow(win)

def open_tour_window():
    win = tk.Toplevel()
    TourWindow(win)

def start_gui():
    root = tk.Tk()
    root.title("Tour Agency Application")
    root.geometry("300x200")

    tk.Button(root, text="Клієнти", width=20, command=open_client_window).pack(pady=10)
    tk.Button(root, text="Тури", width=20, command=open_tour_window).pack(pady=10)

    root.mainloop()
