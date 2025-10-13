import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Admin:
    USERNAME = None
    PASSWORD = None

    @staticmethod
    def Login():
        window = tk.Tk()
        window.configure(bg="white")
        window.geometry("500x400")
        window.title("Login Admin")
        window.resizable(False, False)

        frame = ttk.Frame(window)
        frame.place(x=100, y=100)

        ttk.Label(frame, text="Login Admin", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        Admin.USERNAME = tk.StringVar()
        Admin.PASSWORD = tk.StringVar()

        ttk.Entry(frame, textvariable=Admin.USERNAME, width=30).grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame, text="Username").grid(row=1, column=0, sticky='w')

        ttk.Entry(frame, textvariable=Admin.PASSWORD, width=30, show='*').grid(row=2, column=1, padx=10, pady=5)
        ttk.Label(frame, text="Password").grid(row=2, column=0, sticky='w')

        ttk.Button(frame, text="Login", command=Admin.verifikasi).grid(row=3, column=0, columnspan=2, pady=10)

        window.mainloop()

    @staticmethod
    def verifikasi():
        usr = Admin.USERNAME.get()
        pas = Admin.PASSWORD.get()

        if usr == "admin" and pas == "admin123":
            messagebox.showinfo("Sukses", "Login Admin Berhasil")
            Admin.tampilkan_halaman_zakat()
        else:
            messagebox.showerror("Gagal", "Username atau Password salah")

    @staticmethod
    def tampilkan_halaman_zakat():
        zakat_window = tk.Tk()
        zakat_window.title("Aplikasi Perhitungan Zakat Profesi")
        zakat_window.geometry("500x400")
        zakat_window.configure(bg="white")

        frame = ttk.Frame(zakat_window)
        frame.place(x=50, y=50)

        ttk.Label(frame, text="Perhitungan Zakat Profesi", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        nama = tk.StringVar()
        penghasilan = tk.DoubleVar()
        hasil = tk.StringVar()

        ttk.Label(frame, text="Nama").grid(row=1, column=0, sticky='w')
        ttk.Entry(frame, textvariable=nama, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Penghasilan Bulanan (Rp)").grid(row=2, column=0, sticky='w')
        ttk.Entry(frame, textvariable=penghasilan, width=30).grid(row=2, column=1, pady=5)

        def hitung_zakat():
            gaji = penghasilan.get()
            total_tahunan = gaji * 12
            nisab = 85000000  # asumsi nisab setara 85 gram emas
            if total_tahunan >= nisab:
                zakat = 0.025 * total_tahunan
                hasil.set(f"{nama.get()} wajib zakat sebesar Rp {zakat:,.2f}")
            else:
                hasil.set(f"{nama.get()} tidak wajib zakat (belum mencapai nisab)")

        ttk.Button(frame, text="Hitung Zakat", command=hitung_zakat).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(frame, textvariable=hasil, foreground="blue", wraplength=400).grid(row=4, column=0, columnspan=2, pady=10)

        zakat_window.mainloop()

# Jalankan login admin
if __name__ == "__main__":
    Admin.Login()
