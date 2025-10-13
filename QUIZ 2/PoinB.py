import tkinter as tk
from tkinter import messagebox, ttk

# Fungsi untuk memformat angka ke Rupiah
def format_rupiah(angka):
    return f"Rp. {int(angka):,}".replace(",", ".")

class ManajemenProduk:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Produk")
        self.root.geometry("600x460")
        self.root.configure(bg="#f0f4f7")

        self.editing_mode = False
        self.currently_editing_item = None

        # Judul Aplikasi
        lbl_title = tk.Label(root, text="Manajemen Produk Toko", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#333")
        lbl_title.pack(pady=15)

        # Input Field
        frame_input = tk.Frame(root, bg="#f0f4f7")
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Nama Produk:", bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.nama_entry = tk.Entry(frame_input, width=30)
        self.nama_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_input, text="Harga Produk:", bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.harga_entry = tk.Entry(frame_input, width=30)
        self.harga_entry.grid(row=1, column=1, padx=10, pady=5)

        # Tombol Aksi
        frame_tombol = tk.Frame(root, bg="#f0f4f7")
        frame_tombol.pack(pady=10)

        self.btn_tambah = tk.Button(frame_tombol, text="Tambah Produk", command=self.tambah_produk, bg="#4CAF50", fg="white", width=15)
        self.btn_tambah.grid(row=0, column=0, padx=5)

        self.btn_edit = tk.Button(frame_tombol, text="Edit Produk", command=self.edit_produk, bg="#2196F3", fg="white", width=15)
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_hapus = tk.Button(frame_tombol, text="Hapus Produk", command=self.hapus_produk, bg="#f44336", fg="white", width=15)
        self.btn_hapus.grid(row=0, column=2, padx=5)

        # Tabel Produk
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)

        self.tree = ttk.Treeview(root, columns=("Nama", "Harga"), show="headings", selectmode="browse")
        self.tree.heading("Nama", text="Nama Produk")
        self.tree.heading("Harga", text="Harga Produk")
        self.tree.pack(padx=20, pady=15, fill="x")

        self.tree.bind("<Button-1>", self.block_selection_if_editing)

    # Blok klik saat mode edit aktif
    def block_selection_if_editing(self, event):
        if self.editing_mode:
            messagebox.showinfo("Peringatan", "Selesaikan proses edit sebelum memilih produk lain.")
            return "break"

    # Tambah produk baru
    def tambah_produk(self):
        if self.editing_mode:
            messagebox.showwarning("Peringatan", "Selesaikan edit produk terlebih dahulu.")
            return

        nama = self.nama_entry.get()
        harga = self.harga_entry.get()
        if nama and harga:
            try:
                harga_float = float(harga)
                harga_formatted = format_rupiah(harga_float)
                self.tree.insert("", "end", values=(nama, harga_formatted))
                self.nama_entry.delete(0, tk.END)
                self.harga_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Harga harus berupa angka.")
        else:
            messagebox.showwarning("Peringatan", "Nama dan harga harus diisi.")

    # Mulai proses edit produk
    def edit_produk(self):
        selected = self.tree.selection()
        if self.editing_mode:
            messagebox.showwarning("Peringatan", "Selesaikan edit yang sedang berlangsung terlebih dahulu.")
            return

        if len(selected) != 1:
            messagebox.showwarning("Peringatan", "Pilih tepat satu produk yang ingin diedit.")
            return

        self.editing_mode = True
        self.currently_editing_item = selected[0]

        item = self.tree.item(selected)
        nama, harga = item["values"]

        # Hapus "Rp. " dan titik pada ribuan
        harga_angka = harga.replace("Rp. ", "").replace(".", "")

        self.nama_entry.delete(0, tk.END)
        self.nama_entry.insert(0, nama)
        self.harga_entry.delete(0, tk.END)
        self.harga_entry.insert(0, harga_angka)

        self.btn_tambah.config(state="disabled")
        self.btn_hapus.config(state="disabled")
        self.btn_edit.config(text="Simpan Edit", command=self.simpan_edit)

    # Simpan hasil edit produk
    def simpan_edit(self):
        nama = self.nama_entry.get()
        harga = self.harga_entry.get()

        if not nama or not harga:
            messagebox.showwarning("Peringatan", "Isi nama dan harga produk terlebih dahulu.")
            return

        try:
            harga_float = float(harga)
            harga_formatted = format_rupiah(harga_float)
            self.tree.item(self.currently_editing_item, values=(nama, harga_formatted))
            self.nama_entry.delete(0, tk.END)
            self.harga_entry.delete(0, tk.END)

            self.editing_mode = False
            self.currently_editing_item = None

            self.btn_edit.config(text="Edit Produk", command=self.edit_produk)
            self.btn_tambah.config(state="normal")
            self.btn_hapus.config(state="normal")

        except ValueError:
            messagebox.showerror("Error", "Harga harus berupa angka.")

    # Hapus produk
    def hapus_produk(self):
        if self.editing_mode:
            messagebox.showwarning("Peringatan", "Selesaikan edit terlebih dahulu sebelum menghapus.")
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih produk yang ingin dihapus.")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus produk ini?")
        if confirm:
            for item in selected:
                self.tree.delete(item)

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = ManajemenProduk(root)
    root.mainloop()
