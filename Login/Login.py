import tkinter as tk
from tkinter import messagebox

# Data login yang valid
VALID_USERNAME = "admin"
VALID_PASSWORD = "12345"

# Fungsi halaman setelah login berhasil
def show_hello_world():
    hello_window = tk.Toplevel()  # Membuka jendela baru
    hello_window.title("Halaman Utama")
    hello_window.geometry("300x150")
    tk.Label(hello_window, text="Hello, World!", font=("Arial", 16)).pack(expand=True)

# Fungsi proses login
def login():
    username = entry_user.get()
    password = entry_pass.get()

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
        root.withdraw()  # Menyembunyikan jendela login
        show_hello_world()
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah!")

# GUI Login
root = tk.Tk()
root.title("Login Aplikasi")
root.geometry("300x200")

tk.Label(root, text="Username:").pack(pady=5)
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password:").pack(pady=5)
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()
