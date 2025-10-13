import tkinter as tk
from tkinter import messagebox
import os

# ===== Fungsi Helper =====

def load_users():
    users = {}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                user, pwd = line.strip().split(",")
                users[user] = pwd
    return users

def save_user(username, password):
    with open("users.txt", "a") as f:
        f.write(f"{username},{password}\n")

# ===== Fungsi Login dan Register =====

def login():
    username = entry_user.get()
    password = entry_pass.get()

    if username == "admin" and password == "12345":
        messagebox.showinfo("Login Berhasil", "Selamat datang Admin!")
        root.withdraw()
        show_hello_admin()
    else:
        users = load_users()
        if username in users and users[username] == password:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
            root.withdraw()
            show_hello_user(username)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")

def register():
    reg_user = entry_reg_user.get()
    reg_pass = entry_reg_pass.get()

    users = load_users()
    if reg_user in users:
        messagebox.showerror("Gagal", "Username sudah terdaftar!")
    else:
        save_user(reg_user, reg_pass)
        messagebox.showinfo("Berhasil", "Registrasi berhasil!")
        reg_win.destroy()

def open_register_window():
    global reg_win, entry_reg_user, entry_reg_pass
    reg_win = tk.Toplevel()
    reg_win.title("Registrasi")
    reg_win.geometry("300x200")

    tk.Label(reg_win, text="Username Baru:").pack(pady=5)
    entry_reg_user = tk.Entry(reg_win)
    entry_reg_user.pack()

    tk.Label(reg_win, text="Password Baru:").pack(pady=5)
    entry_reg_pass = tk.Entry(reg_win, show="*")
    entry_reg_pass.pack()

    tk.Button(reg_win, text="Daftar", command=register).pack(pady=15)

# ===== Halaman Selanjutnya =====

def show_hello_admin():
    admin_win = tk.Toplevel()
    admin_win.title("Admin")
    admin_win.geometry("300x150")
    tk.Label(admin_win, text="Hello, Admin!", font=("Arial", 16)).pack(expand=True)

def show_hello_user(username):
    user_win = tk.Toplevel()
    user_win.title("User")
    user_win.geometry("300x150")
    tk.Label(user_win, text=f"Hello, {username}!", font=("Arial", 16)).pack(expand=True)

# ===== GUI Login =====

root = tk.Tk()
root.title("Login Aplikasi")
root.geometry("300x250")

tk.Label(root, text="Username:").pack(pady=5)
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password:").pack(pady=5)
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)
tk.Button(root, text="Register", command=open_register_window).pack()

root.mainloop()
