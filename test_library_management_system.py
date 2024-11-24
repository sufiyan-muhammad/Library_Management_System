import unittest
import json
import os
from io import StringIO
from unittest.mock import patch
from library_management_system import Library  # Assuming your main code is in 'library_management_system.py'

class TestLibrary(unittest.TestCase):
    DATA_FILE = "library_data.json"
    
    def setUp(self):
        """Set up the test environment by initializing the library."""
        if os.path.exists(self.DATA_FILE):
            os.remove(self.DATA_FILE)
        self.library = Library()  # Initialize the library instance

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.DATA_FILE):
            os.remove(self.DATA_FILE)

    def test_add_book(self):
        """Test the functionality to add a book."""
        with patch("builtins.input", side_effect=["Book Title", "Book Author", "2020"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.add_book()
            books = self.library.load_data()
            self.assertEqual(len(books), 1)
            self.assertEqual(books[0]['title'], "Book Title")
            self.assertEqual(books[0]['author'], "Book Author")
            self.assertEqual(books[0]['year'], 2020)
            self.assertEqual(books[0]['status'], "available")
            self.assertIn("Book 'Book Title' added successfully!", mock_stdout.getvalue())

    def test_delete_book(self):
        """Test the functionality to delete a book."""
        with patch("builtins.input", side_effect=["Book Title", "Book Author", "2020"]):
            self.library.add_book()
        with patch("builtins.input", side_effect=["1"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.delete_book()
            books = self.library.load_data()
            self.assertEqual(len(books), 0)
            self.assertIn("Book with ID 1 deleted successfully!", mock_stdout.getvalue())

    def test_delete_non_existent_book(self):
        """Test the case when attempting to delete a non-existent book."""
        with patch("builtins.input", side_effect=["999"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.delete_book()
            self.assertIn("No book found with ID 999.", mock_stdout.getvalue())

    def test_search_book_by_title(self):
        """Test searching for a book by title."""
        with patch("builtins.input", side_effect=["Book Title", "Book Author", "2020"]):
            self.library.add_book()
        with patch("builtins.input", side_effect=["title", "Book Title"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.search_book()
            self.assertIn("ID: 1, Title: Book Title", mock_stdout.getvalue())

    def test_search_book_by_author(self):
        """Test searching for a book by author."""
        with patch("builtins.input", side_effect=["Book Title", "Book Author", "2020"]):
            self.library.add_book()
        with patch("builtins.input", side_effect=["author", "Book Author"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.search_book()
            self.assertIn("ID: 1, Title: Book Title", mock_stdout.getvalue())

    def test_search_book_by_year(self):
        """Test searching for a book by year."""
        with patch("builtins.input", side_effect=["Book Title", "Book Author", "2020"]):
            self.library.add_book()
        with patch("builtins.input", side_effect=["year", "2020"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.search_book()
            self.assertIn("ID: 1, Title: Book Title", mock_stdout.getvalue())

    def test_invalid_search(self):
        """Test searching for a book with invalid criteria."""
        with patch("builtins.input", side_effect=["invalid", "Non-existent Book"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.search_book()
            self.assertIn("Invalid search criteria.", mock_stdout.getvalue())

    def test_change_status_to_issued(self):
        """Test changing the status of a book to 'issued'."""
        with patch("builtins.input", side_effect=["Book Title", "Book Author", "2020"]):
            self.library.add_book()
        with patch("builtins.input", side_effect=["1", "issued"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.change_status()
            books = self.library.load_data()
            self.assertEqual(books[0]['status'], "issued")
            self.assertIn("Status of book with ID 1 updated to 'issued'.", mock_stdout.getvalue())

    def test_change_status_to_invalid(self):
        """Test changing the status of a book to an invalid status."""
        with patch("builtins.input", side_effect=["Book Title", "Book Author", "2020"]):
            self.library.add_book()
        with patch("builtins.input", side_effect=["1", "invalid_status"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.change_status()
            self.assertIn("Invalid status. Please choose 'available' or 'issued'.", mock_stdout.getvalue())

    def test_change_status_for_non_existent_book(self):
        """Test changing the status of a non-existent book."""
        with patch("builtins.input", side_effect=["999", "available"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.change_status()
            self.assertIn("No book found with ID 999.", mock_stdout.getvalue())

    def test_display_books(self):
        """Test displaying all books in the library."""
        with patch("builtins.input", side_effect=["Book Title", "Book Author", "2020"]):
            self.library.add_book()
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.display_books()
            self.assertIn("ID: 1, Title: Book Title", mock_stdout.getvalue())

    def test_display_no_books(self):
        """Test displaying when no books are available."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.library.display_books()
            self.assertIn("No books in the library.", mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()
