"""
Sistema di gestione biblioteca semplificato
"""
from typing import List, Optional, Dict


class Book:
    """Rappresenta un libro nella biblioteca."""
    
    def __init__(self, title: str, author: str, isbn: str):
        """Inizializza un nuovo libro."""
        if not title or not author or not isbn:
            raise ValueError("Titolo, autore e ISBN non possono essere vuoti")
        
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True  # Il libro è disponibile di default
    
    def borrow(self) -> bool:
        """
        Prende in prestito il libro.
        
        Returns:
            bool: True se il libro è stato preso in prestito con successo, False altrimenti
        
        Raises:
            RuntimeError: Se il libro è già in prestito
        """
        if not self.available:
            raise RuntimeError(f"Il libro '{self.title}' è già in prestito")
        
        self.available = False
        return True
    
    def return_book(self) -> bool:
        """
        Restituisce il libro alla biblioteca.
        
        Returns:
            bool: True se il libro è stato restituito con successo, False altrimenti
            
        Raises:
            RuntimeError: Se il libro non è in prestito
        """
        if self.available:
            raise RuntimeError(f"Il libro '{self.title}' non è in prestito")
        
        self.available = True
        return True
    
    def __str__(self) -> str:
        return f"{self.title} di {self.author} ({self.isbn}) - {'Disponibile' if self.available else 'In prestito'}"


class Library:
    """Gestisce una collezione di libri."""
    
    def __init__(self, name: str):
        """Inizializza una nuova biblioteca."""
        self.name = name
        self.books: List[Book] = []
    
    def add_book(self, book: Book) -> bool:
        """
        Aggiunge un libro alla biblioteca.
        
        Args:
            book: Il libro da aggiungere
            
        Returns:
            bool: True se il libro è stato aggiunto con successo
            
        Raises:
            ValueError: Se un libro con lo stesso ISBN è già presente
        """
        # Verifica che il libro non sia già presente tramite ISBN
        if any(existing_book.isbn == book.isbn for existing_book in self.books):
            raise ValueError(f"Un libro con ISBN {book.isbn} è già presente nella biblioteca")
        
        self.books.append(book)
        return True
    
    def search_by_title(self, title: str) -> List[Book]:
        """
        Cerca libri per titolo.
        
        Args:
            title: Il titolo (o parte di esso) da cercare
            
        Returns:
            List[Book]: Lista di libri che corrispondono alla ricerca
        """
        return [book for book in self.books if title.lower() in book.title.lower()]
    
    def search_by_author(self, author: str) -> List[Book]:
        """
        Cerca libri per autore.
        
        Args:
            author: L'autore (o parte del nome) da cercare
            
        Returns:
            List[Book]: Lista di libri che corrispondono alla ricerca
        """
        return [book for book in self.books if author.lower() in book.author.lower()]
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """
        Ottiene un libro tramite ISBN.
        
        Args:
            isbn: L'ISBN del libro da cercare
            
        Returns:
            Optional[Book]: Il libro trovato o None se non esiste
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def borrow_book(self, isbn: str) -> bool:
        """
        Prende in prestito un libro tramite ISBN.
        
        Args:
            isbn: L'ISBN del libro da prendere in prestito
            
        Returns:
            bool: True se il prestito è avvenuto con successo
            
        Raises:
            ValueError: Se il libro non esiste
            RuntimeError: Se il libro è già in prestito
        """
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError(f"Nessun libro trovato con ISBN {isbn}")
        
        return book.borrow()
    
    def return_book(self, isbn: str) -> bool:
        """
        Restituisce un libro tramite ISBN.
        
        Args:
            isbn: L'ISBN del libro da restituire
            
        Returns:
            bool: True se la restituzione è avvenuta con successo
            
        Raises:
            ValueError: Se il libro non esiste
            RuntimeError: Se il libro non è in prestito
        """
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError(f"Nessun libro trovato con ISBN {isbn}")
        
        return book.return_book()
    
    def get_available_books(self) -> List[Book]:
        """
        Ottiene tutti i libri disponibili.
        
        Returns:
            List[Book]: Lista di libri disponibili
        """
        return [book for book in self.books if book.available]
    
    def get_borrowed_books(self) -> List[Book]:
        """
        Ottiene tutti i libri in prestito.
        
        Returns:
            List[Book]: Lista di libri in prestito
        """
        return [book for book in self.books if not book.available]

    def get_statistics(self) -> Dict[str, int]:
        """
        Ottiene statistiche sulla biblioteca.
        
        Returns:
            Dict[str, int]: Dizionario con le statistiche
        """
        return {
            "total_books": len(self.books),
            "available_books": len(self.get_available_books()),
            "borrowed_books": len(self.get_borrowed_books())
        }


# Esempio di utilizzo
if __name__ == "__main__":
    # Crea una biblioteca
    biblioteca = Library("Biblioteca Comunale")
    
    # Aggiungi alcuni libri
    libro1 = Book("Il nome della rosa", "Umberto Eco", "9788845292866")
    libro2 = Book("1984", "George Orwell", "9788804668237")
    libro3 = Book("Il Signore degli Anelli", "J.R.R. Tolkien", "9788830101531")
    
    biblioteca.add_book(libro1)
    biblioteca.add_book(libro2)
    biblioteca.add_book(libro3)
    
    # Cerca libri
    print("Libri di Eco:", [str(libro) for libro in biblioteca.search_by_author("Eco")])
    
    # Prendi in prestito un libro
    biblioteca.borrow_book("9788845292866")
    print("Libri disponibili:", len(biblioteca.get_available_books()))
    print("Libri in prestito:", len(biblioteca.get_borrowed_books()))
    
    # Restituisci un libro
    biblioteca.return_book("9788845292866")
    print("Libri disponibili dopo restituzione:", len(biblioteca.get_available_books()))
