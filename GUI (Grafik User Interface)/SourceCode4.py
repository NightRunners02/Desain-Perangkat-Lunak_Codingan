import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os
from itertools import count

DATABASE_FILE = "database_barang.txt"
TRANSAKSI_FILE = "transaksi.txt"

barang_list = []
transaksi_list = []

def format_rupiah(amount):
    return f"Rp. {int(amount):,}".replace(",", ".")

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
            load_data()
            frame = tk.Frame(main_content, bg="white")

            tree = ttk.Treeview(frame, columns=("Nama", "Harga", "Stok"), show="headings")
            tree.heading("Nama", text="Nama Barang")
            tree.heading("Harga", text="Harga")
            tree.heading("Stok", text="Stok")

            def refresh_tree():
                load_data()
                tree.delete(*tree.get_children())
                for nama, harga, stok in barang_list:
                    tree.insert('', tk.END, values=(nama, format_rupiah(harga), stok))

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
            nama_entry = tk.Entry(frame)
            harga_entry = tk.Entry(frame)
            stok_entry = tk.Entry(frame)

            for label, entry in zip(["Nama:", "Harga:", "Stok:"], [nama_entry, harga_entry, stok_entry]):
                tk.Label(frame, text=label, bg="white").pack()
                entry.pack()

            def tambah():
                try:
                    nama = nama_entry.get()
                    harga = float(harga_entry.get())
                    stok = int(stok_entry.get())
                    barang_list.append((nama, harga, stok))
                    save_data()
                    frame_laporan = create_laporan()
                    SidebarApp.show_frame(main_content, frame_laporan)
                    messagebox.showinfo("Berhasil", "Barang ditambahkan")
                except:
                    messagebox.showerror("Error", "Input tidak valid")

            tk.Button(frame, text="Tambah", command=tambah).pack(pady=10)
            return frame

        def create_laporan_keuangan():
            frame = tk.Frame(main_content, bg="white")
            load_transaksi()
            tk.Label(frame, text="Laporan Keuangan", font=('Segoe UI', 14, 'bold'), bg="white").pack(pady=10)
            tree = ttk.Treeview(frame, columns=("Nama", "Jumlah", "Total"), show="headings")
            for col in ("Nama", "Jumlah", "Total"):
                tree.heading(col, text=col)
            total_pendapatan = 0
            for nama, jumlah, total in transaksi_list:
                tree.insert('', tk.END, values=(nama, jumlah, format_rupiah(total)))
                total_pendapatan += total
            tree.pack(expand=True, fill="both", padx=10, pady=10)
            tk.Label(frame, text=f"Total Uang Masuk: {format_rupiah(total_pendapatan)}", font=('Segoe UI', 12, 'bold'), bg="white").pack(pady=10)
            return frame

        frame_tambah = create_tambah_barang()
        frame_laporan = create_laporan()
        frame_keuangan = create_laporan_keuangan()

        tk.Button(sidebar, text="Tambah Barang", bg="#34495e", fg="white", command=lambda: SidebarApp.show_frame(main_content, frame_tambah)).pack(fill="x", pady=2)
        tk.Button(sidebar, text="Lihat Stok Barang", bg="#34495e", fg="white", command=lambda: SidebarApp.show_frame(main_content, create_laporan())).pack(fill="x", pady=2)
        tk.Button(sidebar, text="Laporan Keuangan", bg="#34495e", fg="white", command=lambda: SidebarApp.show_frame(main_content, frame_keuangan)).pack(fill="x", pady=2)
        tk.Button(sidebar, text="Logout", bg="#e74c3c", fg="white", command=lambda: [root.destroy(), AplikasiLogin.login()]).pack(fill="x", pady=2, side="bottom")

        SidebarApp.show_frame(main_content, frame_laporan)
        root.mainloop()

    @staticmethod
    def kasir_dashboard():
        load_data()

        window = tk.Tk()
        window.title("Dashboard Kasir")
        window.geometry("700x500")
        window.configure(bg="#e0f7fa")

        ttk.Label(window, text="DASHBOARD KASIR", font=('Segoe UI', 18, 'bold')).pack(pady=10)

        tree = ttk.Treeview(window, columns=('Nama', 'Harga', 'Stok'), show='headings')
        for col in ('Nama', 'Harga', 'Stok'):
            tree.heading(col, text=col)

        def refresh_tree():
            load_data()
            tree.delete(*tree.get_children())
            for nama, harga, stok in barang_list:
                tree.insert('', tk.END, values=(nama, format_rupiah(harga), stok))

        def beli_barang():
            selected = tree.selection()
            if selected:
                idx = tree.index(selected[0])
                nama, harga, stok = barang_list[idx]
                jumlah = simpledialog.askinteger("Jumlah", f"Masukkan jumlah beli untuk {nama} (Stok: {stok})")
                if jumlah and 0 < jumlah <= stok:
                    total = jumlah * harga
                    barang_list[idx] = (nama, harga, stok - jumlah)
                    save_data()
                    save_transaksi(nama, jumlah, total)
                    refresh_tree()
                    messagebox.showinfo("Berhasil", f"Pembelian {jumlah} {nama} berhasil. Total: {format_rupiah(total)}")
                else:
                    messagebox.showwarning("Gagal", "Jumlah melebihi stok atau tidak valid")

        refresh_tree()
        tree.pack(padx=20, pady=10, expand=True, fill='both')

        btn_frame = tk.Frame(window, bg="#e0f7fa")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Beli Barang", command=beli_barang).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Refresh Stok", command=refresh_tree).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Logout", command=lambda: [window.destroy(), AplikasiLogin.login()]).pack(side="left", padx=10)

        window.mainloop()

class AplikasiLogin:
    @staticmethod
    def login():
        window = tk.Tk()
        window.title("Login")
        window.geometry("400x500")
        window.configure(bg="#d1f2eb")

        class AnimatedGIF:
            def __init__(self, path, label):
                self.label = label
                self.frames = []
                im = Image.open(path)
                for frame in count(0):
                    try:
                        frame_image = ImageTk.PhotoImage(im.copy().resize((120, 120)))
                        self.frames.append(frame_image)
                        im.seek(frame + 1)
                    except EOFError:
                        break
                self.index = 0
                self.animate()

            def animate(self):
                self.label.config(image=self.frames[self.index])
                self.index = (self.index + 1) % len(self.frames)
                self.label.after(100, self.animate)

        try:
            anim_label = tk.Label(window, bg="#d1f2eb")
            anim_label.pack(pady=10)
            AnimatedGIF("rimuru2.gif", anim_label)
        except:
            tk.Label(window, text="LOGO", font=("Arial", 20), bg="#d1f2eb").pack(pady=20)

        tk.Label(window, text="Login Aplikasi", font=("Segoe UI", 18, "bold"), bg="#d1f2eb").pack(pady=10)

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
