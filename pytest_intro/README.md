# Esercizio: Introduzione a pytest

Questo è un esercizio introduttivo per familiarizzare con pytest, focalizzato su due concetti fondamentali: le fixture e i test parametrizzati.

## Descrizione

In questo esercizio, creeremo e testeremo una semplice classe `Calculator` che può eseguire operazioni matematiche di base e tenere uno storico delle operazioni.

## Concetti di pytest da utilizzare

1. **Fixture**: per preparare oggetti e dati di test
2. **Test parametrizzati**: per testare diversi input e output con un'unica funzione di test
3. **Asserzioni native**: per verificare i risultati

## Obiettivi dell'esercizio

1. Implementare test per i metodi della classe `Calculator`
2. Creare fixture per inizializzare la calcolatrice
3. Parametrizzare i test per le operazioni matematiche
4. Utilizzare fixture con scope diversi
5. Implementare una fixture con pulizia (teardown)

## Come svolgere l'esercizio

1. Installare pytest: `pip install pytest`
2. Studiare il codice nel file `calculator.py`
3. Implementare i test nel file `test_calculator.py` seguendo le istruzioni
4. Eseguire i test con il comando `pytest -v`

## Bonus

- Aggiungere marker personalizzati ai test
- Utilizzare pytest-mock per simulare funzionalità
- Sperimentare con altre caratteristiche di pytest come `skipif` o `xfail`
