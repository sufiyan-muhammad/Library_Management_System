import json
import os


class Library:
    DATA_FILE = "library_data.json"

    def __init__(self):
        self.initialize_library()

    # Initialize library data
    def initialize_library(self):
        if not os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, 'w') as file:
                json.dump([], file)

    # Load library data
    def load_data(self):
        try:
            with open(self.DATA_FILE, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    # Save library data
    def save_data(self, data):
        with open(self.DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)

    # Add a book
    def add_book(self):
        print("\n-- Add Book --")
        title = input("Enter book title: ").strip()
        author = input("Enter book author: ").strip()
        year = input("Enter year of publication: ").strip()

        if not year.isdigit():
            print("Year must be a number!")
            return

        books = self.load_data()
        book_id = len(books) + 1  # Generate unique ID
        book = {
            "id": book_id,
            "title": title,
            "author": author,
            "year": int(year),
            "status": "available"
        }
        books.append(book)
        self.save_data(books)
        print(f"Book '{title}' added successfully!")

    # Delete a book
    def delete_book(self):
        print("\n-- Delete Book --")
        try:
            book_id = int(input("Enter book ID to delete: ").strip())
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        books = self.load_data()
        for book in books:
            if book["id"] == book_id:
                books.remove(book)
                self.save_data(books)
                print(f"Book with ID {book_id} deleted successfully!")
                return

        print(f"No book found with ID {book_id}.")

    # Search for books
    def search_book(self):
        print("\n-- Search Book --")
        criteria = input("Search by (title/author/year): ").strip().lower()
        query = input("Enter search query: ").strip()

        books = self.load_data()
        results = []

        if criteria == "title":
            results = [book for book in books if query.lower() in book["title"].lower()]
        elif criteria == "author":
            results = [book for book in books if query.lower() in book["author"].lower()]
        elif criteria == "year" and query.isdigit():
            results = [book for book in books if book["year"] == int(query)]
        else:
            print("Invalid search criteria.")
            return

        if results:
            print("\nSearch Results:")
            for book in results:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Status: {book['status']}")
        else:
            print("No matching books found.")

    # Display all books
    def display_books(self):
        print("\n-- All Books --")
        books = self.load_data()
        if books:
            for book in books:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Year: {book['year']}, Status: {book['status']}")
        else:
            print("No books in the library.")

    # Change book status
    def change_status(self):
        print("\n-- Change Book Status --")
        try:
            book_id = int(input("Enter book ID: ").strip())
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return

        new_status = input("Enter new status ('available' or 'issued'): ").strip().lower()
        if new_status not in ["available", "issued"]:
            print("Invalid status. Please choose 'available' or 'issued'.")
            return

        books = self.load_data()
        for book in books:
            if book["id"] == book_id:
                book["status"] = new_status
                self.save_data(books)
                print(f"Status of book with ID {book_id} updated to '{new_status}'.")
                return

        print(f"No book found with ID {book_id}.")

    # Main Menu
    def main_menu(self):
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Search Book")
        print("4. Display All Books")
        print("5. Change Book Status")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        return choice

    # Main function
    def run(self):
        while True:
            choice = self.main_menu()
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.delete_book()
            elif choice == '3':
                self.search_book()
            elif choice == '4':
                self.display_books()
            elif choice == '5':
                self.change_status()
            elif choice == '6':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    library = Library()
    library.run()
