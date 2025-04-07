"""
Test unitari per la classe Library
"""
import unittest
from unittest.mock import patch, MagicMock
from main import Library, Book


class TestLibrary(unittest.TestCase):
    """Test per la classe Library."""
    
    def setUp(self):
        """Inizializza una biblioteca e alcuni libri prima di ogni test."""
        # Creiamo una biblioteca
        self.library = Library("Biblioteca di Test")
        
        # Creiamo alcuni libri di esempio
        self.book1 = Book("Il nome della rosa", "Umberto Eco", "9788845292866")
        self.book2 = Book("1984", "George Orwell", "9788804668237")
        self.book3 = Book("Il Signore degli Anelli", "J.R.R. Tolkien", "9788830101531")
    
    def test_init(self):
        """Verifica che l'inizializzazione della biblioteca funzioni correttamente."""
        self.assertEqual(self.library.name, "Biblioteca di Test")
        self.assertEqual(len(self.library.books), 0)  # La biblioteca dovrebbe iniziare vuota
    
    def test_add_book_success(self):
        """Verifica che l'aggiunta di un libro funzioni correttamente."""
        # Aggiungi un libro
        result = self.library.add_book(self.book1)
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        # Verifichiamo che il libro sia stato aggiunto
        self.assertEqual(len(self.library.books), 1)
        self.assertIn(self.book1, self.library.books)
    
    def test_add_book_duplicate_isbn(self):
        """Verifica che aggiungere un libro con ISBN duplicato sollevi un'eccezione."""
        # Prima aggiungiamo un libro
        self.library.add_book(self.book1)
        
        # Creiamo un altro libro con lo stesso ISBN
        duplicate_book = Book("Libro Duplicato", "Autore Diverso", "9788845292866")
        
        # Provare ad aggiungere il libro duplicato dovrebbe sollevare un'eccezione
        with self.assertRaises(ValueError):
            self.library.add_book(duplicate_book)
    
    def test_search_by_title(self):
        """Verifica che la ricerca per titolo funzioni correttamente."""
        # Aggiungiamo alcuni libri
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        
        # Ricerca esatta
        results = self.library.search_by_title("Il nome della rosa")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.book1)
        
        # Ricerca parziale
        results = self.library.search_by_title("Signore")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.book3)
        
        # Ricerca case-insensitive
        results = self.library.search_by_title("nome della rosa")
        self.assertEqual(len(results), 1)
        
        # Ricerca con più risultati
        results = self.library.search_by_title("Il")
        self.assertEqual(len(results), 2)  # "Il nome della rosa" e "Il Signore degli Anelli"
        
        # Ricerca senza risultati
        results = self.library.search_by_title("Libro Inesistente")
        self.assertEqual(len(results), 0)
    
    def test_search_by_author(self):
        """Verifica che la ricerca per autore funzioni correttamente."""
        # Aggiungiamo alcuni libri
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        
        # Ricerca esatta
        results = self.library.search_by_author("Umberto Eco")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.book1)
        
        # Ricerca parziale
        results = self.library.search_by_author("Eco")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.book1)
        
        # Ricerca case-insensitive
        results = self.library.search_by_author("umberto")
        self.assertEqual(len(results), 1)
        
        # Ricerca senza risultati
        results = self.library.search_by_author("Autore Inesistente")
        self.assertEqual(len(results), 0)
    
    def test_get_book_by_isbn(self):
        """Verifica che il recupero di un libro tramite ISBN funzioni correttamente."""
        # Aggiungiamo alcuni libri
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        
        # Recupero di un libro esistente
        book = self.library.get_book_by_isbn("9788845292866")
        self.assertEqual(book, self.book1)
        
        # Recupero di un libro inesistente
        book = self.library.get_book_by_isbn("ISBN-inesistente")
        self.assertIsNone(book)
    
    def test_borrow_book_success(self):
        """Verifica che il prestito di un libro funzioni correttamente."""
        # Aggiungiamo un libro
        self.library.add_book(self.book1)
        
        # Prendiamo in prestito il libro
        result = self.library.borrow_book("9788845292866")
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        # Verifichiamo che il libro non sia più disponibile
        self.assertFalse(self.book1.available)
    
    def test_borrow_book_not_found(self):
        """Verifica che prendere in prestito un libro inesistente sollevi un'eccezione."""
        with self.assertRaises(ValueError):
            self.library.borrow_book("ISBN-inesistente")
    
    def test_borrow_book_not_available(self):
        """Verifica che prendere in prestito un libro già in prestito sollevi un'eccezione."""
        # Aggiungiamo un libro e lo prendiamo in prestito
        self.library.add_book(self.book1)
        self.library.borrow_book("9788845292866")
        
        # Provare a prenderlo di nuovo dovrebbe sollevare un'eccezione
        with self.assertRaises(RuntimeError):
            self.library.borrow_book("9788845292866")
    
    def test_return_book_success(self):
        """Verifica che la restituzione di un libro funzioni correttamente."""
        # Aggiungiamo un libro e lo prendiamo in prestito
        self.library.add_book(self.book1)
        self.library.borrow_book("9788845292866")
        
        # Restituiamo il libro
        result = self.library.return_book("9788845292866")
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        # Verifichiamo che il libro sia nuovamente disponibile
        self.assertTrue(self.book1.available)
    
    def test_return_book_not_found(self):
        """Verifica che restituire un libro inesistente sollevi un'eccezione."""
        with self.assertRaises(ValueError):
            self.library.return_book("ISBN-inesistente")
    
    def test_return_book_not_borrowed(self):
        """Verifica che restituire un libro non in prestito sollevi un'eccezione."""
        # Aggiungiamo un libro (che è disponibile di default)
        self.library.add_book(self.book1)
        
        # Provare a restituirlo dovrebbe sollevare un'eccezione
        with self.assertRaises(RuntimeError):
            self.library.return_book("9788845292866")
    
    def test_get_available_books(self):
        """Verifica che il recupero dei libri disponibili funzioni correttamente."""
        # Aggiungiamo alcuni libri
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        
        # Prendiamo in prestito un libro
        self.library.borrow_book("9788845292866")  # book1
        
        # Recuperiamo i libri disponibili
        available_books = self.library.get_available_books()
        
        # Verifichiamo che ci siano solo i libri disponibili
        self.assertEqual(len(available_books), 2)
        self.assertIn(self.book2, available_books)
        self.assertIn(self.book3, available_books)
        self.assertNotIn(self.book1, available_books)
    
    def test_get_borrowed_books(self):
        """Verifica che il recupero dei libri in prestito funzioni correttamente."""
        # Aggiungiamo alcuni libri
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        
        # Prendiamo in prestito due libri
        self.library.borrow_book("9788845292866")  # book1
        self.library.borrow_book("9788804668237")  # book2
        
        # Recuperiamo i libri in prestito
        borrowed_books = self.library.get_borrowed_books()
        
        # Verifichiamo che ci siano solo i libri in prestito
        self.assertEqual(len(borrowed_books), 2)
        self.assertIn(self.book1, borrowed_books)
        self.assertIn(self.book2, borrowed_books)
        self.assertNotIn(self.book3, borrowed_books)
    
    def test_get_statistics(self):
        """Verifica che il recupero delle statistiche funzioni correttamente."""
        # Biblioteca vuota
        stats = self.library.get_statistics()
        self.assertEqual(stats["total_books"], 0)
        self.assertEqual(stats["available_books"], 0)
        self.assertEqual(stats["borrowed_books"], 0)
        
        # Aggiungiamo alcuni libri
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        
        # Prendiamo in prestito un libro
        self.library.borrow_book("9788845292866")  # book1
        
        # Verifichiamo le statistiche
        stats = self.library.get_statistics()
        self.assertEqual(stats["total_books"], 3)
        self.assertEqual(stats["available_books"], 2)
        self.assertEqual(stats["borrowed_books"], 1)


if __name__ == '__main__':
    unittest.main()
