"""
Test di integrazione per il sistema di gestione biblioteca
"""
import unittest
from main import Book, Library


class TestLibraryIntegration(unittest.TestCase):
    """Test di integrazione per il sistema di gestione biblioteca."""
    
    def setUp(self):
        """Inizializza una biblioteca e alcuni libri prima di ogni test."""
        # Creiamo una biblioteca
        self.library = Library("Biblioteca Comunale")
        
        # Creiamo alcuni libri di esempio
        self.books = [
            Book("Il nome della rosa", "Umberto Eco", "9788845292866"),
            Book("1984", "George Orwell", "9788804668237"),
            Book("Il Signore degli Anelli", "J.R.R. Tolkien", "9788830101531"),
            Book("Harry Potter", "J.K. Rowling", "9788867158188"),
            Book("Il Codice da Vinci", "Dan Brown", "9788804687288")
        ]
    
    def test_complete_library_workflow(self):
        """Verifica un flusso di lavoro completo della biblioteca."""
        # 1. Aggiungiamo tutti i libri alla biblioteca
        for book in self.books:
            self.library.add_book(book)
        
        # Verifichiamo che tutti i libri siano stati aggiunti
        self.assertEqual(len(self.library.books), len(self.books))
        
        # 2. Cerchiamo libri per titolo
        fantasy_books = self.library.search_by_title("Signore")
        self.assertEqual(len(fantasy_books), 1)
        
        # 3. Cerchiamo libri per autore
        rowling_books = self.library.search_by_author("Rowling")
        self.assertEqual(len(rowling_books), 1)
        self.assertEqual(rowling_books[0].title, "Harry Potter")
        
        # 4. Prendiamo in prestito alcuni libri
        self.library.borrow_book("9788845292866")  # Il nome della rosa
        self.library.borrow_book("9788804668237")  # 1984
        
        # Verifichiamo che i libri siano in prestito
        borrowed_books = self.library.get_borrowed_books()
        self.assertEqual(len(borrowed_books), 2)
        
        # Verifichiamo che i libri non siano più disponibili
        for book in borrowed_books:
            self.assertFalse(book.available)
        
        # 5. Restituiamo un libro
        self.library.return_book("9788845292866")  # Il nome della rosa
        
        # Verifichiamo che il libro sia di nuovo disponibile
        book = self.library.get_book_by_isbn("9788845292866")
        self.assertTrue(book.available)
        
        # Verifichiamo che solo un libro rimanga in prestito
        borrowed_books = self.library.get_borrowed_books()
        self.assertEqual(len(borrowed_books), 1)
        self.assertEqual(borrowed_books[0].isbn, "9788804668237")  # 1984
        
        # 6. Verifichiamo le statistiche
        stats = self.library.get_statistics()
        self.assertEqual(stats["total_books"], 5)
        self.assertEqual(stats["available_books"], 4)
        self.assertEqual(stats["borrowed_books"], 1)
    
    def test_multiple_users_scenario(self):
        """Simula uno scenario con più utenti che prendono in prestito e restituiscono libri."""
        # Aggiungiamo tutti i libri alla biblioteca
        for book in self.books:
            self.library.add_book(book)
        
        # Simuliamo il prestito di libri a diversi utenti
        # Utente 1: prende in prestito "Il nome della rosa" e "Harry Potter"
        self.library.borrow_book("9788845292866")  # Il nome della rosa
        self.library.borrow_book("9788867158188")  # Harry Potter
        
        # Utente 2: prova a prendere in prestito "Il nome della rosa" (già in prestito)
        with self.assertRaises(RuntimeError):
            self.library.borrow_book("9788845292866")
        
        # Utente 2: prende in prestito "Il Codice da Vinci"
        self.library.borrow_book("9788804687288")  # Il Codice da Vinci
        
        # Verifichiamo che 3 libri siano in prestito
        borrowed_books = self.library.get_borrowed_books()
        self.assertEqual(len(borrowed_books), 3)
        
        # Utente 1: restituisce "Harry Potter"
        self.library.return_book("9788867158188")
        
        # Utente 3: ora può prendere in prestito "Harry Potter"
        self.library.borrow_book("9788867158188")
        
        # Verifichiamo che le statistiche siano corrette
        stats = self.library.get_statistics()
        self.assertEqual(stats["total_books"], 5)
        self.assertEqual(stats["available_books"], 2)
        self.assertEqual(stats["borrowed_books"], 3)


if __name__ == '__main__':
    unittest.main()
