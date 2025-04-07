# Soluzione: Sistema di Gestione Biblioteca

Questa soluzione mostra come implementare test per un sistema di gestione biblioteca. Vengono illustrati diversi tipi di test, dalle unità più piccole (classe Book) all'integrazione tra componenti.

## Struttura dei test

La soluzione è organizzata in tre file principali:

1. `test_book.py`: Test unitari per la classe Book
2. `test_library.py`: Test unitari per la classe Library
3. `test_integration.py`: Test di integrazione che verificano l'interazione tra componenti

## Tecniche di testing utilizzate

### 1. Test setup con setUp()

In ogni classe di test utilizziamo il metodo `setUp()` per preparare l'ambiente di test prima di ogni metodo di test. Questo approccio garantisce che ogni test parta da uno stato pulito e prevedibile:

```python
def setUp(self):
    """Inizializza un libro prima di ogni test."""
    self.book = Book("Il nome della rosa", "Umberto Eco", "9788845292866")
```

### 2. Test delle eccezioni

Utilizziamo il context manager `assertRaises` per verificare che vengano sollevate le eccezioni appropriate:

```python
with self.assertRaises(ValueError):
    Book("", "Umberto Eco", "9788845292866")  # Titolo vuoto
```

### 3. Verifica dello stato degli oggetti

Dopo un'operazione, verifichiamo che lo stato dell'oggetto sia cambiato correttamente:

```python
# Proviamo a prenderlo in prestito
result = self.book.borrow()
        
# Verifichiamo che l'operazione abbia avuto successo
self.assertTrue(result)
# Verifichiamo che lo stato del libro sia cambiato a non disponibile
self.assertFalse(self.book.available)
```

### 4. Test di casi normali e casi limite

Per ogni funzionalità testiamo:
- Casi normali (il comportamento atteso quando tutto funziona correttamente)
- Casi limite (comportamento con input al limite dell'accettabile)
- Gestione degli errori (comportamento quando qualcosa va storto)

### 5. Test di integrazione

I test di integrazione verificano il funzionamento combinato delle classi Book e Library in scenari realistici:

```python
def test_complete_library_workflow(self):
    """Verifica un flusso di lavoro completo della biblioteca."""
    # 1. Aggiungiamo tutti i libri alla biblioteca
    # 2. Cerchiamo libri per titolo
    # 3. Cerchiamo libri per autore
    # 4. Prendiamo in prestito alcuni libri
    # 5. Restituiamo un libro
    # 6. Verifichiamo le statistiche
```

## Spiegazione dei test unitari per Book

### test_init_valid / test_init_invalid
Verificano che l'inizializzazione della classe Book funzioni correttamente con parametri validi e sollevi eccezioni con parametri non validi. Controllano che:
- Gli attributi siano impostati correttamente
- Un nuovo libro sia disponibile per impostazione predefinita
- Vengano sollevate eccezioni quando titolo, autore o ISBN sono vuoti

### test_borrow_available / test_borrow_not_available
Testano il metodo `borrow()`:
- Verificano che un libro disponibile possa essere preso in prestito
- Verificano che lo stato del libro cambi da disponibile a non disponibile
- Verificano che un'eccezione venga sollevata quando si prova a prendere in prestito un libro non disponibile

### test_return_borrowed / test_return_not_borrowed
Testano il metodo `return_book()`:
- Verificano che un libro in prestito possa essere restituito
- Verificano che lo stato del libro cambi da non disponibile a disponibile
- Verificano che un'eccezione venga sollevata quando si prova a restituire un libro non in prestito

### test_str_representation
Verifica che la rappresentazione in stringa del libro contenga le informazioni corrette e si aggiorni quando lo stato del libro cambia.

## Spiegazione dei test unitari per Library

### test_init
Verifica che l'inizializzazione della classe Library funzioni correttamente, impostando il nome e creando una lista vuota di libri.

### test_add_book_success / test_add_book_duplicate_isbn
Testano il metodo `add_book()`:
- Verificano che un libro possa essere aggiunto alla biblioteca
- Verificano che venga sollevata un'eccezione quando si prova ad aggiungere un libro con un ISBN già presente

### test_search_by_title / test_search_by_author
Testano i metodi di ricerca:
- Ricerca esatta (titolo/autore completo)
- Ricerca parziale (parte del titolo/autore)
- Ricerca case-insensitive
- Ricerca con più risultati
- Ricerca senza risultati

### test_get_book_by_isbn
Verifica che un libro possa essere recuperato tramite ISBN e che venga restituito None per un ISBN inesistente.

### test_borrow_book_* / test_return_book_*
Testano i metodi di prestito e restituzione:
- Verificano che un libro possa essere preso in prestito e restituito
- Verificano che vengano sollevate eccezioni appropriate quando:
  - Il libro non esiste
  - Il libro è già in prestito
  - Il libro non è in prestito

### test_get_available_books / test_get_borrowed_books
Verificano che i metodi restituiscano correttamente le liste dei libri disponibili e in prestito.

### test_get_statistics
Verifica che le statistiche della biblioteca (totale libri, libri disponibili, libri in prestito) siano corrette.

## Esecuzione dei test

Per eseguire i test, utilizzare i seguenti comandi:

```bash
# Esegui tutti i test
python -m unittest discover -s solutions

# Esegui solo i test per la classe Book
python -m unittest solutions.test_book

# Esegui solo i test per la classe Library
python -m unittest solutions.test_library

# Esegui solo i test di integrazione
python -m unittest solutions.test_integration
```

## Conclusioni

Questa soluzione dimostra:
1. Come testare in modo approfondito le unità individuali di un sistema
2. Come verificare l'integrazione tra componenti
3. Come utilizzare `unittest` per organizzare e strutturare i test
4. Come gestire i test di scenari complessi e realistici

Seguendo questo approccio, possiamo avere maggiore fiducia nel nostro codice e nella sua capacità di gestire correttamente vari scenari d'uso.
