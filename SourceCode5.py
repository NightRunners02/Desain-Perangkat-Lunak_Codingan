import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

DATABASE_FILE = "database_barang.txt"
TRANSAKSI_FILE = "transaksi.txt"

barang_list = []
transaksi_list = []

def load_data():
    global barang_list
    barang_list = []
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    nama, harga, stok = parts
                    try:
                        barang_list.append((nama, float(harga), int(stok)))
                    except:
                        pass

def save_data():
    with open(DATABASE_FILE, "w") as f:
        for nama, harga, stok in barang_list:
            f.write(f"{nama}|{harga}|{stok}\n")

def save_transaksi(nama_barang, jumlah, total):
    with open(TRANSAKSI_FILE, "a") as f:
        f.write(f"{nama_barang}|{jumlah}|{total}\n")

def load_transaksi():
    global transaksi_list
    transaksi_list = []
    if os.path.exists(TRANSAKSI_FILE):
        with open(TRANSAKSI_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    transaksi_list.append((parts[0], int(parts[1]), float(parts[2])))

class SidebarApp:
    @staticmethod
    def show_frame(frame_container, frame_to_show):
        for widget in frame_container.winfo_children():
            widget.pack_forget()
        frame_to_show.pack(expand=True, fill="both")

    @staticmethod
    def admin_dashboard():
        load_data()
        root = tk.Tk()
        root.title("Admin Dashboard")
        root.geometry("950x600")
        root.configure(bg="white")

        sidebar = tk.Frame(root, width=200, bg="#2c3e50")
        sidebar.pack(side="left", fill="y")

        main_content = tk.Frame(root, bg="white")
        main_content.pack(side="right", expand=True, fill="both")

        def create_laporan():
            frame = tk.Frame(main_content, bg="white")

            tree = ttk.Treeview(frame, columns=("Nama", "Harga", "Stok"), show="headings")
            tree.heading("Nama", text="Nama Barang")
            tree.heading("Harga", text="Harga")
            tree.heading("Stok", text="Stok")

            def refresh_tree():
                tree.delete(*tree.get_children())
                for nama, harga, stok in barang_list:
                    tree.insert('', tk.END, values=(nama, harga, stok))

            def hapus_barang():
                selected = tree.selection()
                if selected:
                    idx = tree.index(selected[0])
                    barang_list.pop(idx)
                    save_data()
                    refresh_tree()
                    messagebox.showinfo("Info", "Barang berhasil dihapus.")

            def edit_barang():
                selected = tree.selection()
                if selected:
                    idx = tree.index(selected[0])
                    nama, harga, stok = barang_list[idx]
                    edit_win = tk.Toplevel(frame)
                    edit_win.title("Edit Barang")

                    tk.Label(edit_win, text="Nama").pack()
                    nama_entry = tk.Entry(edit_win)
                    nama_entry.insert(0, nama)
                    nama_entry.pack()

                    tk.Label(edit_win, text="Harga").pack()
                    harga_entry = tk.Entry(edit_win)
                    harga_entry.insert(0, harga)
                    harga_entry.pack()

                    tk.Label(edit_win, text="Stok").pack()
                    stok_entry = tk.Entry(edit_win)
                    stok_entry.insert(0, stok)
                    stok_entry.pack()

                    def simpan():
                        try:
                            new_nama = nama_entry.get()
                            new_harga = float(harga_entry.get())
                            new_stok = int(stok_entry.get())
                            barang_list[idx] = (new_nama, new_harga, new_stok)
                            save_data()
                            refresh_tree()
                            edit_win.destroy()
                        except:
                            messagebox.showerror("Error", "Input tidak valid")

                    tk.Button(edit_win, text="Simpan", command=simpan).pack(pady=10)

            refresh_tree()
            tree.pack(expand=True, fill="both", padx=10, pady=10)

            btn_frame = tk.Frame(frame, bg="white")
            btn_frame.pack(pady=5)
            tk.Button(btn_frame, text="Edit Barang", command=edit_barang).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Hapus Barang", command=hapus_barang).pack(side="left", padx=5)

            return frame

        def create_tambah_barang():
            frame = tk.Frame(main_content, bg="white")
            tk.Label(frame, text="Tambah Barang", font=('Segoe UI', 14, 'bold'), bg="white").pack(pady=10)
            tk.Label(frame, text="Nama:", bg="white").pack()
            nama_entry = tk.Entry(frame)
            nama_entry.pack()
            tk.Label(frame, text="Harga:", bg="white").pack()
            harga_entry = tk.Entry(frame)
            harga_entry.pack()
            tk.Label(frame, text="Stok:", bg="white").pack()
            stok_entry = tk.Entry(frame)
            stok_entry.pack()
            def tambah():
                try:
                    nama = nama_entry.get()
                    harga = float(harga_entry.get())
                    stok = int(stok_entry.get())
                    barang_list.append((nama, harga, stok))
                    save_data()
                    messagebox.showinfo("Berhasil", "Barang ditambahkan")
                    nama_entry.delete(0, tk.END)
                    harga_entry.delete(0, tk.END)
                    stok_entry.delete(0, tk.END)
                except:
                    messagebox.showerror("Error", "Input tidak valid")
            tk.Button(frame, text="Tambah", command=tambah).pack(pady=10)
            return frame

        def create_laporan_keuangan():
            frame = tk.Frame(main_content, bg="white")
            load_transaksi()
            tk.Label(frame, text="Laporan Keuangan", font=('Segoe UI', 14, 'bold'), bg="white").pack(pady=10)
            tree = ttk.Treeview(frame, columns=("Nama", "Jumlah", "Total"), show="headings")
            tree.heading("Nama", text="Nama Barang")
            tree.heading("Jumlah", text="Jumlah")
            tree.heading("Total", text="Total")
            total_pendapatan = 0
            for nama, jumlah, total in transaksi_list:
                tree.insert('', tk.END, values=(nama, jumlah, total))
                total_pendapatan += total
            tree.pack(expand=True, fill="both", padx=10, pady=10)
            tk.Label(frame, text=f"Total Uang Masuk: Rp {total_pendapatan}", font=('Segoe UI', 12, 'bold'), bg="white").pack(pady=10)
            return frame

        frame_tambah = create_tambah_barang()
        frame_laporan = create_laporan()
        frame_keuangan = create_laporan_keuangan()

        tk.Button(sidebar, text="Tambah Barang", bg="#34495e", fg="white", command=lambda: SidebarApp.show_frame(main_content, frame_tambah)).pack(fill="x", pady=2)
        tk.Button(sidebar, text="Lihat Stok Barang", bg="#34495e", fg="white", command=lambda: SidebarApp.show_frame(main_content, frame_laporan)).pack(fill="x", pady=2)
        tk.Button(sidebar, text="Laporan Keuangan", bg="#34495e", fg="white", command=lambda: SidebarApp.show_frame(main_content, frame_keuangan)).pack(fill="x", pady=2)
        tk.Button(sidebar, text="Logout", bg="#e74c3c", fg="white", command=root.destroy).pack(fill="x", pady=2, side="bottom")

        SidebarApp.show_frame(main_content, frame_laporan)
        root.mainloop()

    @staticmethod
    def kasir_dashboard():
        load_data()  # Pastikan data terbaru dimuat

        window = tk.Tk()
        window.title("Dashboard Kasir")
        window.geometry("600x500")
        window.configure(bg="white")

        ttk.Label(window, text="DASHBOARD KASIR", font=('Segoe UI', 16, 'bold')).pack(pady=10)

        frame = ttk.Frame(window)
        frame.pack(pady=10, fill='both', expand=True)

        ttk.Label(frame, text="Daftar Barang:", font=('Segoe UI', 12, 'bold')).pack()

        tree = ttk.Treeview(frame, columns=('Nama', 'Harga'), show='headings')
        tree.heading('Nama', text='Nama Barang')
        tree.heading('Harga', text='Harga')

        for nama, harga in barang_list:
            tree.insert('', tk.END, values=(nama, harga))

        tree.pack(expand=True, fill='both', padx=10, pady=10)

        ttk.Button(window, text="Logout", width=20, command=window.destroy).pack(pady=20)

        window.mainloop()
          # Gunakan implementasi dashboard kasir yang sudah kamu punya
        pass
class AplikasiLogin:
    @staticmethod
    def login():
        window = tk.Tk()
        window.configure(bg="white")
        window.geometry("400x500")
        window.title("Login")
        window.resizable(False, False)

        try:
            img = Image.open("rimuru.png")
            img = img.resize((80, 80))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(window, image=photo, bg="white")
            label.image = photo
            label.pack(pady=10)
        except:
            pass

        tk.Label(window, text="Login Aplikasi", font=("Segoe UI", 18, "bold"), bg="white").pack(pady=10)

        username_var = tk.StringVar()
        password_var = tk.StringVar()
        role_var = tk.StringVar()

        ttk.Entry(window, textvariable=username_var, font=("Segoe UI", 12)).pack(pady=10)
        ttk.Entry(window, textvariable=password_var, font=("Segoe UI", 12), show="*").pack(pady=10)
        ttk.Combobox(window, textvariable=role_var, values=["Admin", "Kasir"], state="readonly").pack(pady=10)

        def verifikasi():
            usr = username_var.get()
            pas = password_var.get()
            role = role_var.get()
            if role == "Admin" and usr == "admin" and pas == "admin123":
                window.destroy()
                SidebarApp.admin_dashboard()
            elif role == "Kasir" and usr == "kasir" and pas == "kasir123":
                window.destroy()
                SidebarApp.kasir_dashboard()
            else:
                messagebox.showerror("Login Gagal", "Username atau Password salah")

        ttk.Button(window, text="Login", command=verifikasi).pack(pady=20)
        window.mainloop()

if __name__ == "__main__":
    AplikasiLogin.login()
