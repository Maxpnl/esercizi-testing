# Esercizio 2: Carrello Acquisti Online

Questo esercizio riguarda lo sviluppo di test per un sistema di carrello per acquisti online.

## Descrizione

Il file `main.py` contiene un'implementazione di un sistema di carrello acquisti con diverse classi:
- `Product`: rappresenta un prodotto con nome, prezzo e disponibilità
- `ShoppingCart`: gestisce gli articoli aggiunti al carrello
- `PaymentProcessor`: simula l'elaborazione dei pagamenti
- `OrderService`: gestisce il processo di ordine completo

## Obiettivi dell'esercizio

1. Scrivere test unitari per la classe `Product`
   - Testare che l'inizializzazione e le proprietà funzionino correttamente
   - Verificare che le eccezioni vengano sollevate per input non validi

2. Scrivere test unitari per la classe `ShoppingCart`
   - Testare l'aggiunta di prodotti al carrello
   - Testare la rimozione di prodotti dal carrello
   - Testare il calcolo del totale (con e senza sconti)
   - Verificare che le eccezioni siano generate correttamente

3. Scrivere test unitari con mock per `PaymentProcessor`
   - Testare l'elaborazione dei pagamenti simulando API esterne
   - Usare `unittest.mock` per sostituire le chiamate esterne

4. Scrivere test di integrazione per `OrderService`
   - Testare il flusso completo di un ordine
   - Usare mock per isolare le dipendenze esterne

## Suggerimenti

- Usa `unittest.mock` per simulare chiamate API al servizio di pagamento
- Verifica che gli errori di pagamento vengano gestiti correttamente
- Testa i casi limite (carrello vuoto, prodotti non disponibili, ecc.)
- Assicurati che tutti i metodi vengano testati sia per i successi che per i fallimenti

## Bonus

- Aggiungi test parametrizzati per verificare il comportamento con diversi input
- Implementa e testa una funzionalità di codice promozionale per sconti aggiuntivi
