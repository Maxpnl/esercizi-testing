# Soluzione: Sistema di Carrello Acquisti Online

Questa soluzione dimostra come implementare test completi per un sistema di e-commerce che include prodotti, carrello della spesa, elaborazione pagamenti e gestione ordini. La soluzione mostra diverse tecniche di testing: test unitari, mocking di dipendenze esterne, e test di integrazione.

## Struttura dei test

La soluzione è organizzata in quattro file principali:

1. `test_product.py`: Test unitari per la classe Product
2. `test_shopping_cart.py`: Test unitari per la classe ShoppingCart
3. `test_payment_processor.py`: Test unitari con mock per la classe PaymentProcessor
4. `test_order_service.py`: Test unitari e di integrazione per la classe OrderService

## Tecniche di testing utilizzate

### 1. Test Setup con setUp()

In ogni classe di test utilizziamo il metodo `setUp()` per preparare l'ambiente di test prima di ogni metodo:

```python
def setUp(self):
    """Inizializza un carrello e alcuni prodotti prima di ogni test."""
    # Creiamo un carrello vuoto
    self.cart = ShoppingCart()
    
    # Creiamo alcuni prodotti di esempio
    self.product1 = Product("p1", "Laptop", 999.99, 5)
    self.product2 = Product("p2", "Mouse", 29.99, 20)
```

### 2. Mocking di dipendenze esterne

Utilizziamo i mock per sostituire comportamenti che sono:
- Non deterministici (come random.random())
- Lenti (come time.sleep())
- Dipendenze esterne (come API di pagamento)

```python
@patch('time.sleep')  # Mock per evitare il ritardo durante i test
@patch('random.random')  # Mock per controllare la simulazione di successo/fallimento
def test_process_payment_success(self, mock_random, mock_sleep):
    # Impostiamo il mock per simulare sempre un successo
    mock_random.return_value = 0.5  # Valore inferiore a 0.9 per il successo
    mock_sleep.return_value = None  # Evita di attendere durante i test
```

### 3. Mocking di classi intere

Utilizziamo `MagicMock` per sostituire completamente una classe:

```python
# Creiamo un mock del processore di pagamenti
self.mock_payment_processor = MagicMock(spec=PaymentProcessor)
        
# Creiamo un servizio ordini con il mock del processore
self.order_service = OrderService(self.mock_payment_processor)
```

### 4. Verifica delle eccezioni

Utilizziamo context manager `assertRaises` per verificare che vengano sollevate le eccezioni appropriate:

```python
# Quantità zero
with self.assertRaises(ValueError):
    self.cart.add_product(self.product1, 0)
```

### 5. Test di integrazione

Per i test di integrazione, combiniamo più componenti per verificare il loro funzionamento insieme:

```python
@patch('time.sleep')
@patch('random.random')
def test_complete_order_workflow(self, mock_random, mock_sleep):
    """Verifica un flusso di lavoro completo di ordine e annullamento."""
    # ...
```

## Spiegazione dettagliata dei test

### Test per la classe Product

#### Validazioni di inizializzazione
Verifichiamo che:
- Gli attributi vengano impostati correttamente
- Vengano sollevate eccezioni per prezzi non validi (zero o negativi)
- Vengano sollevate eccezioni per stock negativo

#### Controllo disponibilità
Testiamo:
- La disponibilità con stock sufficiente
- La disponibilità con stock insufficiente
- La disponibilità con vari livelli di quantità

#### Operazioni di stock
Verifichiamo:
- La corretta riduzione dello stock durante una prenotazione
- Il rifiuto di prenotazioni quando lo stock è insufficiente
- Il corretto incremento dello stock durante un rifornimento
- Il rifiuto di rifornimenti con quantità negative

### Test per la classe ShoppingCart

#### Gestione prodotti nel carrello
Testiamo:
- L'aggiunta di prodotti al carrello
- L'aggiornamento della quantità quando si aggiunge un prodotto già presente
- La rimozione parziale di prodotti
- La rimozione completa di prodotti
- La gestione di errori (quantità non valide, stock insufficiente)

#### Calcolo del totale
Verifichiamo:
- Il calcolo del totale senza sconti
- Il calcolo del totale con sconti applicati
- Il totale zero per un carrello vuoto

#### Applicazione sconti
Testiamo:
- L'applicazione corretta di sconti
- Il rifiuto di percentuali di sconto non valide (negative o superiori a 100)

#### Operazioni di checkout
Verifichiamo:
- La generazione corretta della lista di checkout
- Il rifiuto del checkout con carrello vuoto
- La verifica della disponibilità attuale durante il checkout

### Test per la classe PaymentProcessor

#### Elaborazione pagamenti
Testiamo:
- Il successo dell'elaborazione del pagamento
- Il fallimento dell'elaborazione del pagamento
- La gestione dei campi mancanti nei dettagli di pagamento

#### Elaborazione rimborsi
Verifichiamo:
- Il successo dell'elaborazione del rimborso
- Il fallimento dell'elaborazione del rimborso
- La validazione dell'ID transazione

#### Tecniche di mocking utilizzate
Mostriamo:
- Come mockare `time.sleep()` per evitare ritardi nei test
- Come mockare `random.random()` per controllare il comportamento simulato
- Come mockare `print()` per verificare i messaggi di output

### Test per la classe OrderService

#### Test unitari con mock
Testiamo:
- La creazione di ordini con successo
- La gestione degli errori (carrello vuoto, dettagli utente mancanti)
- La gestione dei fallimenti di pagamento
- Il recupero di ordini esistenti e non esistenti
- L'annullamento di ordini e i relativi rimborsi

#### Test di integrazione
Verifichiamo:
- Il flusso completo di un ordine: dalla creazione all'annullamento
- Il flusso con fallimento del pagamento

## Concetti chiave dimostrati

### 1. Isolamento dei test
Ogni test deve verificare una singola funzionalità o comportamento, in modo che se un test fallisce, il problema sia facilmente identificabile.

### 2. Gestione delle dipendenze
Utilizziamo i mock per sostituire dipendenze esterne o comportamenti non deterministici, in modo da rendere i test deterministici e isolati.

### 3. Test di successo e fallimento
Testiamo sia i casi di successo (happy path) che i casi di fallimento (error handling).

### 4. Livelli di test
Dimostriamo diversi livelli di test: unitari (singole classi), di integrazione (interazione tra classi) e di sistema (flussi completi di utilizzo).

### 5. Organizzazione dei test
Ogni test segue una struttura chiara:
- **Arrange**: Preparazione dell'ambiente e dei dati di test
- **Act**: Esecuzione dell'operazione da testare
- **Assert**: Verifica dei risultati attesi

## Esecuzione dei test

Per eseguire i test, utilizzare i seguenti comandi:

```bash
# Esegui tutti i test
python -m unittest discover -s solutions

# Esegui solo i test per una specifica classe
python -m unittest solutions.test_product
python -m unittest solutions.test_shopping_cart
python -m unittest solutions.test_payment_processor
python -m unittest solutions.test_order_service
```

## Conclusioni

Questa soluzione dimostra:
1. Come testare in modo approfondito un sistema e-commerce complesso
2. Come utilizzare mock per isolare le unità di test dalle dipendenze esterne
3. Come verificare comportamenti sia normali che eccezionali
4. Come combinare test unitari e di integrazione per una copertura completa

L'approccio mostrato consente di sviluppare sistemi robusti e affidabili, riducendo il rischio di bug e semplificando la manutenzione e l'evoluzione del codice nel tempo.
