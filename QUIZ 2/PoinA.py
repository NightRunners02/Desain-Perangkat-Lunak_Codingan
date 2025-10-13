import tkinter as tk
from tkinter import messagebox

# Format angka ke rupiah
def format_rupiah(angka):
    return f"Rp. {int(angka):,}".replace(",", ".")

class KembalianApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hitung Kembalian")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f4f7")

        # Judul
        title = tk.Label(root, text="Kalkulator Kembalian", font=("Helvetica", 16, "bold"), bg="#f0f4f7")
        title.pack(pady=15)

        # Input Frame
        frame_input = tk.Frame(root, bg="#f0f4f7")
        frame_input.pack(pady=10)

        # Total Belanja
        tk.Label(frame_input, text="Total Belanja (Rp):", bg="#f0f4f7").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.entry_total = tk.Entry(frame_input, width=25)
        self.entry_total.grid(row=0, column=1, pady=5)

        # Uang Diberikan
        tk.Label(frame_input, text="Uang Diberikan (Rp):", bg="#f0f4f7").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_uang = tk.Entry(frame_input, width=25)
        self.entry_uang.grid(row=1, column=1, pady=5)

        # Tombol Hitung
        btn_hitung = tk.Button(root, text="Hitung Kembalian", command=self.hitung_kembalian, bg="#2196F3", fg="white", width=20)
        btn_hitung.pack(pady=10)

        # Output Label
        self.label_hasil = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f4f7", fg="green")
        self.label_hasil.pack(pady=10)

    def hitung_kembalian(self):
        total = self.entry_total.get()
        uang = self.entry_uang.get()

        try:
            total = float(total)
            uang = float(uang)

            if uang < total:
                messagebox.showwarning("Uang Kurang", "Uang yang diberikan tidak cukup untuk membayar.")
                self.label_hasil.config(text="")
            else:
                kembalian = uang - total
                hasil = format_rupiah(kembalian)
                self.label_hasil.config(text=f"Kembalian: {hasil}")
        except ValueError:
            messagebox.showerror("Input Salah", "Masukkan angka yang valid pada kedua kolom.")

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = KembalianApp(root)
    root.mainloop()
