import tkinter as tk
from tkinter import messagebox

def get_nishab_emas(harga_emas_per_gram):
    return 85 * harga_emas_per_gram

def hitung_zakat_profesi(gaji_bulanan, harga_emas):
    penghasilan_tahunan = gaji_bulanan * 12
    nishab = get_nishab_emas(harga_emas)
    if penghasilan_tahunan >= nishab:
        return 0.025 * penghasilan_tahunan
    else:
        return 0

def hitung_zakat_mal(total_harta, harga_emas):
    nishab = get_nishab_emas(harga_emas)
    if total_harta >= nishab:
        return 0.025 * total_harta
    else:
        return 0

def hitung_zakat():
    try:
        harga_emas = float(entry_harga_emas.get())
        pilihan = zakat_var.get()

        if pilihan == "profesi":
            gaji = float(entry_gaji.get())
            zakat = hitung_zakat_profesi(gaji, harga_emas)
            if zakat > 0:
                result.set(f"Zakat Profesi: Rp{zakat:,.2f}")
            else:
                result.set("Penghasilan belum mencapai nishab.")
        elif pilihan == "mal":
            harta = float(entry_harta.get())
            zakat = hitung_zakat_mal(harta, harga_emas)
            if zakat > 0:
                result.set(f"Zakat Mal: Rp{zakat:,.2f}")
            else:
                result.set("Harta belum mencapai nishab.")
    except ValueError:
        messagebox.showerror("Input Salah", "Mohon masukkan angka yang valid.")

# Setup GUI
root = tk.Tk()
root.title("Aplikasi Perhitungan Zakat")
root.geometry("400x350")

zakat_var = tk.StringVar(value="profesi")
result = tk.StringVar()

tk.Label(root, text="Harga Emas per Gram:").pack()
entry_harga_emas = tk.Entry(root)
entry_harga_emas.pack()

tk.Label(root, text="Pilih Jenis Zakat:").pack()
tk.Radiobutton(root, text="Zakat Profesi", variable=zakat_var, value="profesi").pack()
tk.Radiobutton(root, text="Zakat Mal", variable=zakat_var, value="mal").pack()

# Bagian zakat profesi
tk.Label(root, text="Gaji Bulanan (Zakat Profesi):").pack()
entry_gaji = tk.Entry(root)
entry_gaji.pack()

# Bagian zakat mal
tk.Label(root, text="Total Harta (Zakat Mal):").pack()
entry_harta = tk.Entry(root)
entry_harta.pack()

tk.Button(root, text="Hitung Zakat", command=hitung_zakat).pack(pady=10)
tk.Label(root, textvariable=result, font=("Arial", 12, "bold")).pack()

root.mainloop()
