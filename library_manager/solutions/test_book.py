"""
Test unitari per la classe Book
"""
import unittest
from main import Book


class TestBook(unittest.TestCase):
    """Test per la classe Book."""
    
    def setUp(self):
        """Inizializza un libro prima di ogni test."""
        # Prepariamo un libro valido che potremo utilizzare in più test
        self.book = Book("Il nome della rosa", "Umberto Eco", "9788845292866")
    
    def test_init_valid(self):
        """Verifica che l'inizializzazione funzioni correttamente con parametri validi."""
        # Verifichiamo che gli attributi siano impostati correttamente
        self.assertEqual(self.book.title, "Il nome della rosa")
        self.assertEqual(self.book.author, "Umberto Eco")
        self.assertEqual(self.book.isbn, "9788845292866")
        self.assertTrue(self.book.available)  # Un nuovo libro dovrebbe essere disponibile
    
    def test_init_invalid(self):
        """Verifica che l'inizializzazione sollevi eccezioni con parametri non validi."""
        # Testiamo che vengano sollevate eccezioni con valori vuoti
        with self.assertRaises(ValueError):
            Book("", "Umberto Eco", "9788845292866")  # Titolo vuoto
        
        with self.assertRaises(ValueError):
            Book("Il nome della rosa", "", "9788845292866")  # Autore vuoto
        
        with self.assertRaises(ValueError):
            Book("Il nome della rosa", "Umberto Eco", "")  # ISBN vuoto
    
    def test_borrow_available(self):
        """Verifica che il metodo borrow funzioni quando il libro è disponibile."""
        # Il libro è disponibile per impostazione predefinita
        self.assertTrue(self.book.available)
        
        # Proviamo a prenderlo in prestito
        result = self.book.borrow()
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        # Verifichiamo che lo stato del libro sia cambiato a non disponibile
        self.assertFalse(self.book.available)
    
    def test_borrow_not_available(self):
        """Verifica che borrow sollevi un'eccezione quando il libro non è disponibile."""
        # Prima prendiamo il libro in prestito
        self.book.borrow()
        
        # Ora il libro non è disponibile, quindi provare a prenderlo di nuovo
        # dovrebbe sollevare un'eccezione
        with self.assertRaises(RuntimeError):
            self.book.borrow()
    
    def test_return_borrowed(self):
        """Verifica che return_book funzioni quando il libro è in prestito."""
        # Prima prendiamo il libro in prestito
        self.book.borrow()
        # Verifichiamo che non sia disponibile
        self.assertFalse(self.book.available)
        
        # Proviamo a restituirlo
        result = self.book.return_book()
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        # Verifichiamo che lo stato del libro sia cambiato a disponibile
        self.assertTrue(self.book.available)
    
    def test_return_not_borrowed(self):
        """Verifica che return_book sollevi un'eccezione quando il libro non è in prestito."""
        # Il libro è disponibile per impostazione predefinita
        self.assertTrue(self.book.available)
        
        # Provare a restituire un libro che non è in prestito dovrebbe sollevare un'eccezione
        with self.assertRaises(RuntimeError):
            self.book.return_book()
    
    def test_str_representation(self):
        """Verifica che la rappresentazione in stringa sia corretta."""
        # Verifichiamo che la stringa contenga le informazioni del libro
        book_str = str(self.book)
        self.assertIn("Il nome della rosa", book_str)
        self.assertIn("Umberto Eco", book_str)
        self.assertIn("9788845292866", book_str)
        self.assertIn("Disponibile", book_str)  # Il libro è disponibile
        
        # Prendiamo il libro in prestito e verifichiamo che cambi la stringa
        self.book.borrow()
        book_str = str(self.book)
        self.assertIn("In prestito", book_str)  # Ora il libro è in prestito


if __name__ == '__main__':
    unittest.main()
