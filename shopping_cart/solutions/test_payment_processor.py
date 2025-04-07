"""
Test unitari per la classe PaymentProcessor
"""
import unittest
from unittest.mock import patch, MagicMock
import time
import random
from main import PaymentProcessor


class TestPaymentProcessor(unittest.TestCase):
    """Test per la classe PaymentProcessor."""
    
    def setUp(self):
        """Inizializza un processore di pagamenti prima di ogni test."""
        self.processor = PaymentProcessor(api_key="test_api_key")
        
        # Creiamo dei dettagli di pagamento validi da utilizzare nei test
        self.valid_payment_details = {
            "card_number": "4111111111111111",
            "expiry": "12/25",
            "cvv": "123"
        }
    
    def test_init(self):
        """Verifica che l'inizializzazione del processore funzioni correttamente."""
        self.assertEqual(self.processor.api_key, "test_api_key")
    
    @patch('time.sleep')  # Mock per evitare il ritardo durante i test
    @patch('random.random')  # Mock per controllare la simulazione di successo/fallimento
    def test_process_payment_success(self, mock_random, mock_sleep):
        """Verifica che process_payment funzioni correttamente in caso di successo."""
        # Impostiamo il mock per simulare sempre un successo
        mock_random.return_value = 0.5  # Valore inferiore a 0.9 per il successo
        mock_sleep.return_value = None  # Evita di attendere durante i test
        
        # Eseguiamo il pagamento
        result = self.processor.process_payment(100.0, self.valid_payment_details)
        
        # Verifichiamo che il risultato sia corretto
        self.assertTrue(result["success"])
        self.assertIn("transaction_id", result)
        self.assertEqual(result["amount"], 100.0)
        self.assertIn("timestamp", result)
        
        # Verifichiamo che time.sleep sia stato chiamato
        mock_sleep.assert_called_once_with(0.5)
    
    @patch('time.sleep')  # Mock per evitare il ritardo durante i test
    @patch('random.random')  # Mock per controllare la simulazione di successo/fallimento
    def test_process_payment_failure(self, mock_random, mock_sleep):
        """Verifica che process_payment sollevi un'eccezione in caso di fallimento."""
        # Impostiamo il mock per simulare sempre un fallimento
        mock_random.return_value = 0.95  # Valore superiore a 0.9 per il fallimento
        mock_sleep.return_value = None  # Evita di attendere durante i test
        
        # Verifichiamo che venga sollevata un'eccezione
        with self.assertRaises(RuntimeError):
            self.processor.process_payment(100.0, self.valid_payment_details)
        
        # Verifichiamo che time.sleep sia stato chiamato
        mock_sleep.assert_called_once_with(0.5)
    
    def test_process_payment_missing_fields(self):
        """Verifica che process_payment sollevi un'eccezione con campi mancanti."""
        # Dettagli di pagamento incompleti
        incomplete_details = {
            "card_number": "4111111111111111",
            # Manca expiry
            "cvv": "123"
        }
        
        # Verifichiamo che venga sollevata un'eccezione
        with self.assertRaises(ValueError):
            self.processor.process_payment(100.0, incomplete_details)
    
    @patch('time.sleep')  # Mock per evitare il ritardo durante i test
    @patch('random.random')  # Mock per controllare la simulazione di successo/fallimento
    def test_refund_payment_success(self, mock_random, mock_sleep):
        """Verifica che refund_payment funzioni correttamente in caso di successo."""
        # Impostiamo il mock per simulare sempre un successo
        mock_random.return_value = 0.5  # Valore inferiore a 0.95 per il successo
        mock_sleep.return_value = None  # Evita di attendere durante i test
        
        # Eseguiamo il rimborso
        result = self.processor.refund_payment("txn_123456")
        
        # Verifichiamo che il risultato sia corretto
        self.assertTrue(result["success"])
        self.assertIn("refund_id", result)
        self.assertEqual(result["transaction_id"], "txn_123456")
        self.assertIn("timestamp", result)
        
        # Verifichiamo che time.sleep sia stato chiamato
        mock_sleep.assert_called_once_with(0.5)
    
    @patch('time.sleep')  # Mock per evitare il ritardo durante i test
    @patch('random.random')  # Mock per controllare la simulazione di successo/fallimento
    def test_refund_payment_failure(self, mock_random, mock_sleep):
        """Verifica che refund_payment sollevi un'eccezione in caso di fallimento."""
        # Impostiamo il mock per simulare sempre un fallimento
        mock_random.return_value = 0.99  # Valore superiore a 0.95 per il fallimento
        mock_sleep.return_value = None  # Evita di attendere durante i test
        
        # Verifichiamo che venga sollevata un'eccezione
        with self.assertRaises(RuntimeError):
            self.processor.refund_payment("txn_123456")
        
        # Verifichiamo che time.sleep sia stato chiamato
        mock_sleep.assert_called_once_with(0.5)
    
    def test_refund_payment_invalid_transaction_id(self):
        """Verifica che refund_payment sollevi un'eccezione con ID transazione non valido."""
        # ID transazione non valido
        with self.assertRaises(ValueError):
            self.processor.refund_payment("invalid_id")  # Non inizia con "txn_"
    
    def test_process_payment_with_mocked_print(self):
        """Verifica process_payment con print mockato."""
        # Creiamo un context manager per mockare la funzione print
        with patch('builtins.print') as mock_print:
            # Utilizziamo i patch esistenti per time.sleep e random.random
            with patch('time.sleep'):
                with patch('random.random', return_value=0.5):
                    # Eseguiamo il pagamento
                    self.processor.process_payment(100.0, self.valid_payment_details)
                    
                    # Verifichiamo che print sia stato chiamato con il messaggio corretto
                    mock_print.assert_called_once_with("Elaborazione pagamento di €100.00...")
                    
    def test_refund_payment_with_mocked_print(self):
        """Verifica refund_payment con print mockato."""
        # Creiamo un context manager per mockare la funzione print
        with patch('builtins.print') as mock_print:
            # Utilizziamo i patch esistenti per time.sleep e random.random
            with patch('time.sleep'):
                with patch('random.random', return_value=0.5):
                    # Eseguiamo il rimborso
                    self.processor.refund_payment("txn_123456")
                    
                    # Verifichiamo che print sia stato chiamato con il messaggio corretto
                    mock_print.assert_called_once_with("Elaborazione rimborso per la transazione txn_123456...")


if __name__ == '__main__':
    unittest.main()
