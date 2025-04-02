"""
Un modulo semplice per una calcolatrice che mantiene uno storico delle operazioni.
"""
from typing import List, Tuple, Dict, Optional, Any
import math


class Calculator:
    """
    Una calcolatrice semplice che può eseguire operazioni matematiche di base
    e tenere traccia della storia delle operazioni.
    """
    
    def __init__(self, precision: int = 2):
        """
        Inizializza una nuova calcolatrice.
        
        Args:
            precision: Il numero di cifre decimali da mantenere nei risultati.
        """
        if precision < 0:
            raise ValueError("La precisione non può essere negativa")
        
        self.precision = precision
        self.history: List[Dict[str, Any]] = []
        self.memory: Optional[float] = None
    
    def _add_to_history(self, operation: str, a: float, b: Optional[float] = None, result: float = 0) -> None:
        """
        Aggiunge un'operazione alla storia.
        
        Args:
            operation: Nome dell'operazione eseguita.
            a: Primo operando.
            b: Secondo operando (se applicabile).
            result: Risultato dell'operazione.
        """
        entry = {
            "operation": operation,
            "a": a,
            "result": round(result, self.precision)
        }
        
        if b is not None:
            entry["b"] = b
            
        self.history.append(entry)
    
    def add(self, a: float, b: float) -> float:
        """
        Addizione di due numeri.
        
        Args:
            a: Primo addendo.
            b: Secondo addendo.
            
        Returns:
            La somma di a e b.
        """
        result = a + b
        self._add_to_history("add", a, b, result)
        return round(result, self.precision)
    
    def subtract(self, a: float, b: float) -> float:
        """
        Sottrazione di due numeri.
        
        Args:
            a: Minuendo.
            b: Sottraendo.
            
        Returns:
            La differenza tra a e b.
        """
        result = a - b
        self._add_to_history("subtract", a, b, result)
        return round(result, self.precision)
    
    def multiply(self, a: float, b: float) -> float:
        """
        Moltiplicazione di due numeri.
        
        Args:
            a: Primo fattore.
            b: Secondo fattore.
            
        Returns:
            Il prodotto di a e b.
        """
        result = a * b
        self._add_to_history("multiply", a, b, result)
        return round(result, self.precision)
    
    def divide(self, a: float, b: float) -> float:
        """
        Divisione di due numeri.
        
        Args:
            a: Dividendo.
            b: Divisore.
            
        Returns:
            Il quoziente di a e b.
            
        Raises:
            ZeroDivisionError: Se b è zero.
        """
        if b == 0:
            raise ZeroDivisionError("Impossibile dividere per zero")
        
        result = a / b
        self._add_to_history("divide", a, b, result)
        return round(result, self.precision)
    
    def square_root(self, a: float) -> float:
        """
        Calcola la radice quadrata di un numero.
        
        Args:
            a: Il numero di cui calcolare la radice quadrata.
            
        Returns:
            La radice quadrata di a.
            
        Raises:
            ValueError: Se a è negativo.
        """
        if a < 0:
            raise ValueError("Impossibile calcolare la radice quadrata di un numero negativo")
        
        result = math.sqrt(a)
        self._add_to_history("square_root", a, result=result)
        return round(result, self.precision)
    
    def power(self, a: float, b: float) -> float:
        """
        Calcola a elevato alla potenza b.
        
        Args:
            a: La base.
            b: L'esponente.
            
        Returns:
            a elevato alla potenza b.
        """
        result = a ** b
        self._add_to_history("power", a, b, result)
        return round(result, self.precision)
    
    def store_in_memory(self, value: float) -> None:
        """
        Memorizza un valore nella memoria della calcolatrice.
        
        Args:
            value: Il valore da memorizzare.
        """
        self.memory = value
    
    def recall_from_memory(self) -> Optional[float]:
        """
        Recupera il valore memorizzato.
        
        Returns:
            Il valore memorizzato o None se la memoria è vuota.
        """
        return self.memory
    
    def clear_memory(self) -> None:
        """Cancella il valore memorizzato."""
        self.memory = None
    
    def clear_history(self) -> None:
        """Cancella la storia delle operazioni."""
        self.history.clear()
    
    def get_last_operation(self) -> Optional[Dict[str, Any]]:
        """
        Ottiene l'ultima operazione eseguita.
        
        Returns:
            Un dizionario con i dettagli dell'operazione o None se la storia è vuota.
        """
        if not self.history:
            return None
        
        return self.history[-1]
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Ottiene la storia completa delle operazioni.
        
        Returns:
            Una lista di dizionari con i dettagli delle operazioni.
        """
        return self.history
