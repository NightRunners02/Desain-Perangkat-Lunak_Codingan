import tkinter as tk  # import library GUI tkinter
from tkinter import ttk  # library input frame

# Memulai tampilan
window = tk.Tk()

# Properties
window.configure(bg="white")
window.geometry("500x800")
window.title("Aplikasi Saya")

# Frame dalam window
input_frame = ttk.Frame(window)
input_frame.pack(padx=10, fill="x", expand=True)

# Label inputan
nama_depan_label = ttk.Label(input_frame, text="Pesan:")
nama_depan_label.pack(padx=10, fill="x", expand=True)

# Input
PESAN = tk.StringVar()  # variabel pesan
nama_depan_input = ttk.Entry(input_frame, textvariable=PESAN)
nama_depan_input.pack(padx=10, fill="x", expand=True)

# Fungsi saat tombol diklik
def tombol_klik():
    isi_pesan = PESAN.get()
    hasil_pesan = ttk.Label(input_frame, text=isi_pesan)
    hasil_pesan.pack(padx=10, fill="x", expand=True)

# Tombol
tombol_kirim = ttk.Button(input_frame, text="Kirim", command=tombol_klik)
tombol_kirim.pack(padx=10, pady=10, fill="x", expand=True)

# Menjalankan aplikasi
window.mainloop()
