class Library:
    def __init__(self):
        self.books = {
            1: {"title": "Python Basics", "author": "John Doe", "available": True},
            2: {"title": "Advanced Python", "author": "Jane Doe", "available": True},
            3: {"title": "Data Science Basics", "author": "Alice Smith", "available": True},
            4: {"title": "Machine Learning", "author": "Bob Brown", "available": True},
            5: {"title": "Deep Learning", "author": "Charlie Green", "available": True}
        }
        self.members = {}
        self.borrowed_books = {}

    def register_member(self, member_id, name):
        self.members[member_id] = name

    def display_books(self):
        print("\nDaftar Buku:")
        for book_id, details in self.books.items():
            status = "Tersedia" if details["available"] else "Dipinjam"
            print(f"{book_id}: {details['title']} - {details['author']} ({status})")
    
    def display_borrowed_books(self):
        print("\nBuku yang sedang dipinjam:")
        if not self.borrowed_books:
            print("Tidak ada buku yang sedang dipinjam.")
        else:
            for book_id, member_id in self.borrowed_books.items():
                print(f"{book_id}: {self.books[book_id]['title']} - Dipinjam oleh {self.members[member_id]}")

    def borrow_book(self, member_id):
        self.display_books()
        book_id = int(input("Masukkan ID buku yang ingin dipinjam: "))
        if book_id in self.books and self.books[book_id]["available"]:
            self.books[book_id]["available"] = False
            self.borrowed_books[book_id] = member_id
            print(f"{self.members[member_id]} meminjam '{self.books[book_id]['title']}'")
        else:
            print("Buku tidak tersedia atau tidak ada.")

    def return_book(self):
        self.display_borrowed_books()
        book_id = int(input("Masukkan ID buku yang ingin dikembalikan: "))
        if book_id in self.borrowed_books:
            self.books[book_id]["available"] = True
            del self.borrowed_books[book_id]
            print("Buku berhasil dikembalikan.")
        else:
            print("Buku tidak sedang dipinjam.")

# Contoh penggunaan
library = Library()
library.register_member(101, "Alice")

while True:
    print("\n1. Pinjam Buku")
    print("2. Kembalikan Buku")
    print("3. Lihat Buku yang Dipinjam")
    print("4. Keluar")
    pilihan = input("Pilih opsi: ")
    if pilihan == "1":
        library.borrow_book(101)
    elif pilihan == "2":
        library.return_book()
    elif pilihan == "3":
        library.display_borrowed_books()
    elif pilihan == "4":
        break
    else:
        print("Pilihan tidak valid.")