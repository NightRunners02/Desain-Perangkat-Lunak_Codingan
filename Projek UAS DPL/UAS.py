import tkinter as tk
from tkinter import messagebox, ttk

# Data login dummy
login_data = {
    "mahasiswa": {"username": "mahasiswa", "password": "123"},
    "admin": {"username": "admin", "password": "admin"},
    "kemahasiswaan": {"username": "kemahasiswaan", "password": "kemahasiswaan"},
}

# Simpan data PKM sementara
pkm_submissions = []

# Fungsi validasi login

def validate_login(role, user_entry, pass_entry, root):
    username = user_entry.get()
    password = pass_entry.get()
    if username == login_data[role]['username'] and password == login_data[role]['password']:
        root.destroy()
        if role == "mahasiswa":
            mahasiswa_dashboard()
        elif role == "admin":
            admin_dashboard()
        elif role == "kemahasiswaan":
            kemahasiswaan_dashboard()
    else:
        messagebox.showerror("Login Gagal", "Username atau Password salah")

# Tampilan login

def login_page(role):
    login = tk.Tk()
    login.title(f"Login {role.capitalize()}")
    login.geometry("400x300")
    login.config(bg="#e3f2fd")

    tk.Label(login, text=f"Login Sebagai {role.capitalize()}", font=("Helvetica", 16, "bold"), bg="#e3f2fd").pack(pady=10)

    frame = tk.Frame(login, bg="#bbdefb", bd=2, relief="groove")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    tk.Label(frame, text="Username:", bg="#bbdefb").pack(pady=5)
    user_entry = tk.Entry(frame)
    user_entry.pack()

    tk.Label(frame, text="Password:", bg="#bbdefb").pack(pady=5)
    pass_entry = tk.Entry(frame, show='*')
    pass_entry.pack()

    tk.Button(frame, text="Login", command=lambda: validate_login(role, user_entry, pass_entry, login), bg="#64b5f6", fg="white", width=15).pack(pady=15)
    login.mainloop()

# Dashboard Mahasiswa

def mahasiswa_dashboard():
    root = tk.Tk()
    root.title("Dashboard Mahasiswa")
    root.geometry("600x500")
    root.config(bg="#e8f5e9")

    def submit_pkm():
        judul = judul_entry.get()
        anggota = anggota_entry.get()
        jenis = jenis_var.get()
        if judul and anggota and jenis:
            pkm_submissions.append({
                "judul": judul,
                "anggota": anggota,
                "jenis": jenis,
                "status": "Menunggu Validasi",
                "catatan": ""
            })
            messagebox.showinfo("Berhasil", "PKM berhasil dikirim")
            refresh_list()
        else:
            messagebox.showerror("Error", "Lengkapi semua data")

    def refresh_list():
        listbox.delete(0, tk.END)
        for i, pkm in enumerate(pkm_submissions):
            listbox.insert(tk.END, f"{i+1}. {pkm['judul']} - {pkm['status']}")

    def edit_selected():
        selected = listbox.curselection()
        if selected:
            idx = selected[0]
            judul_entry.delete(0, tk.END)
            anggota_entry.delete(0, tk.END)
            jenis_var.set(pkm_submissions[idx]['jenis'])
            judul_entry.insert(0, pkm_submissions[idx]['judul'])
            anggota_entry.insert(0, pkm_submissions[idx]['anggota'])
            pkm_submissions[idx]['status'] = "Diedit oleh Mahasiswa"
            refresh_list()

    tk.Label(root, text="Form Pengajuan PKM", font=("Helvetica", 16, "bold"), bg="#e8f5e9").pack(pady=10)
    form_frame = tk.Frame(root, bg="#c8e6c9", bd=2, relief="groove")
    form_frame.pack(padx=10, pady=5, fill="both")

    tk.Label(form_frame, text="Judul PKM:", bg="#c8e6c9").pack(pady=5)
    judul_entry = tk.Entry(form_frame)
    judul_entry.pack(fill="x", padx=10)

    tk.Label(form_frame, text="Anggota Kelompok:", bg="#c8e6c9").pack(pady=5)
    anggota_entry = tk.Entry(form_frame)
    anggota_entry.pack(fill="x", padx=10)

    jenis_var = tk.StringVar(value="PKMK")
    tk.Label(form_frame, text="Jenis PKM:", bg="#c8e6c9").pack(pady=5)
    jenis_menu = ttk.Combobox(form_frame, textvariable=jenis_var, values=["PKMK", "PKMT", "PKMM", "PKMP"])
    jenis_menu.pack(fill="x", padx=10)

    tk.Button(form_frame, text="Kirim", command=submit_pkm, bg="#66bb6a", fg="white").pack(pady=10)
    tk.Button(form_frame, text="Edit Pilihan", command=edit_selected, bg="#ffa726").pack(pady=5)

    listbox = tk.Listbox(root, height=8)
    listbox.pack(fill="both", padx=10, pady=10)

    refresh_list()
    root.mainloop()

# Dashboard Admin

def admin_dashboard():
    root = tk.Tk()
    root.title("Dashboard Admin")
    root.geometry("500x400")
    root.config(bg="#f3e5f5")

    tk.Label(root, text="Rekap Data PKM", font=("Helvetica", 16, "bold"), bg="#f3e5f5").pack(pady=10)
    for pkm in pkm_submissions:
        info = f"Judul: {pkm['judul']} | Status: {pkm['status']}"
        tk.Label(root, text=info, bg="#f3e5f5").pack(anchor="w", padx=20)

    root.mainloop()

# Dashboard Kemahasiswaan

def kemahasiswaan_dashboard():
    root = tk.Tk()
    root.title("Validasi PKM - Kemahasiswaan")
    root.geometry("600x500")
    root.config(bg="#fff3e0")

    tk.Label(root, text="Validasi dan Masukan PKM", font=("Helvetica", 16, "bold"), bg="#fff3e0").pack(pady=10)

    listbox = tk.Listbox(root, height=10)
    listbox.pack(fill="both", padx=10, pady=5)

    for i, pkm in enumerate(pkm_submissions):
        listbox.insert(tk.END, f"{i+1}. {pkm['judul']} - {pkm['status']}")

    catatan_entry = tk.Entry(root, width=50)
    catatan_entry.pack(pady=5)

    def validasi():
        selected = listbox.curselection()
        if selected:
            idx = selected[0]
            catatan = catatan_entry.get()
            pkm_submissions[idx]['catatan'] = catatan
            pkm_submissions[idx]['status'] = "Disetujui Kemahasiswaan"
            listbox.delete(idx)
            listbox.insert(idx, f"{idx+1}. {pkm_submissions[idx]['judul']} - {pkm_submissions[idx]['status']}")
            messagebox.showinfo("Sukses", "PKM telah divalidasi dan dicatat")

    tk.Button(root, text="Validasi & Simpan Catatan", command=validasi, bg="#ef6c00", fg="white").pack(pady=10)
    root.mainloop()

# Menu awal memilih role

def main_menu():
    menu = tk.Tk()
    menu.title("Sistem PKM - Login Awal")
    menu.geometry("400x300")
    menu.config(bg="#e1f5fe")

    tk.Label(menu, text="Selamat Datang di Sistem PKM", font=("Helvetica", 16, "bold"), bg="#e1f5fe").pack(pady=20)

    tk.Button(menu, text="Login Mahasiswa", command=lambda: login_page("mahasiswa"), width=20, bg="#81d4fa").pack(pady=10)
    tk.Button(menu, text="Login Admin", command=lambda: login_page("admin"), width=20, bg="#9575cd").pack(pady=10)
    tk.Button(menu, text="Login Kemahasiswaan", command=lambda: login_page("kemahasiswaan"), width=20, bg="#ffb74d").pack(pady=10)

    menu.mainloop()

main_menu()