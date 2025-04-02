# Esercizio 1: Sistema di Gestione Biblioteca

Questo esercizio riguarda lo sviluppo di test per un sistema di gestione di una biblioteca.

## Descrizione

Il file `main.py` contiene una semplice implementazione di un sistema di gestione biblioteca con due classi:
- `Book`: rappresenta un libro con titolo, autore e disponibilità
- `Library`: gestisce una collezione di libri con funzionalità per aggiungere, cercare e prestare libri

## Obiettivi dell'esercizio

1. Scrivere test unitari per la classe `Book`
   - Testare i metodi `borrow` e `return_book`
   - Verificare che le eccezioni vengano sollevate correttamente

2. Scrivere test unitari per la classe `Library`
   - Testare l'aggiunta di libri
   - Testare la ricerca di libri per titolo e autore
   - Testare il prestito e la restituzione dei libri
   - Verificare che le eccezioni vengano sollevate correttamente
   - Usare `unittest.mock` per simulare il comportamento di Book

3. Scrivere test di integrazione
   - Testare l'interazione tra `Library` e `Book`
   - Verificare scenari completi (aggiunta libro, ricerca, prestito, restituzione)

## Suggerimenti

- Applica la struttura vista nelle slides con `setUp` per preparare l'ambiente di test
- Verifica sia i casi positivi che quelli negativi (gestione errori)
- Testa i casi limite (ad esempio, prestare un libro già in prestito)

## Bonus

- Usa `patch.object` per testare i metodi della classe `Library` in isolamento
