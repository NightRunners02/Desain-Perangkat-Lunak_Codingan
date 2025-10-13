class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.borrowed_books = {}

    def register_member(self, member_id, name):
        self.members[member_id] = name

    def add_book(self, book_id, title, author, rack):
        self.books[book_id] = {"title": title, "author": author, "rack": rack, "available": True}

    def search_book(self, title=None, author=None):
        results = [book for book in self.books.values() if (title in book['title'] or author in book['author'])]
        return results

    def borrow_book(self, member_id, book_id):
        if book_id in self.books and self.books[book_id]["available"]:
            self.books[book_id]["available"] = False
            self.borrowed_books[book_id] = member_id
            return f"{self.members[member_id]} borrowed '{self.books[book_id]['title']}'"
        return "Book not available or doesn't exist"

    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            self.books[book_id]["available"] = True
            del self.borrowed_books[book_id]
            return "Book returned successfully"
        return "Book was not borrowed"

    def report_borrowed_books(self):
        return {book_id: self.books[book_id] for book_id in self.borrowed_books}

    def report_new_books(self):
        return self.books

# Example Usage
library = Library()
library.register_member(101, "Alice")
library.add_book(1, "Python Basics", "John Doe", "A1")
library.add_book(2, "Advanced Python", "Jane Doe", "B2")

print(library.borrow_book(101, 1))
print(library.return_book(1))
print(library.report_borrowed_books())