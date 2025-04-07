"""
Test unitari e di integrazione per la classe OrderService
"""
import unittest
from unittest.mock import patch, MagicMock
from main import OrderService, PaymentProcessor, ShoppingCart, Product


class TestOrderService(unittest.TestCase):
    """Test per la classe OrderService."""
    
    def setUp(self):
        """Inizializza un servizio ordini, un carrello e alcuni prodotti prima di ogni test."""
        # Creiamo un mock del processore di pagamenti
        self.mock_payment_processor = MagicMock(spec=PaymentProcessor)
        
        # Creiamo un servizio ordini con il mock del processore
        self.order_service = OrderService(self.mock_payment_processor)
        
        # Creiamo un carrello
        self.cart = ShoppingCart()
        
        # Creiamo alcuni prodotti di esempio
        self.product1 = Product("p1", "Laptop", 999.99, 5)
        self.product2 = Product("p2", "Mouse", 29.99, 20)
        
        # Creiamo dettagli utente validi
        self.valid_user_details = {
            "name": "Mario Rossi",
            "email": "mario.rossi@example.com",
            "address": "Via Roma 123, Milano"
        }
        
        # Creiamo dettagli di pagamento validi
        self.valid_payment_details = {
            "card_number": "4111111111111111",
            "expiry": "12/25",
            "cvv": "123"
        }
    
    def test_init(self):
        """Verifica che l'inizializzazione del servizio ordini funzioni correttamente."""
        self.assertEqual(self.order_service.payment_processor, self.mock_payment_processor)
        self.assertEqual(len(self.order_service.orders), 0)  # Nessun ordine iniziale
    
    def test_place_order_empty_cart(self):
        """Verifica che place_order sollevi un'eccezione con carrello vuoto."""
        with self.assertRaises(ValueError):
            self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
    
    def test_place_order_missing_user_details(self):
        """Verifica che place_order sollevi un'eccezione con dettagli utente mancanti."""
        # Aggiungiamo un prodotto al carrello
        self.cart.add_product(self.product1, 1)
        
        # Dettagli utente incompleti
        incomplete_user_details = {
            "name": "Mario Rossi",
            # Manca email
            "address": "Via Roma 123, Milano"
        }
        
        # Verifichiamo che venga sollevata un'eccezione
        with self.assertRaises(ValueError):
            self.order_service.place_order(self.cart, incomplete_user_details, self.valid_payment_details)
    
    def test_place_order_payment_failure(self):
        """Verifica che place_order sollevi un'eccezione se il pagamento fallisce."""
        # Aggiungiamo un prodotto al carrello
        self.cart.add_product(self.product1, 1)
        
        # Configuriamo il mock per simulare un fallimento di pagamento
        self.mock_payment_processor.process_payment.side_effect = RuntimeError("Pagamento fallito: la transazione è stata rifiutata")
        
        # Verifichiamo che venga sollevata un'eccezione
        with self.assertRaises(RuntimeError):
            self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
        
        # Verifichiamo che il processo di pagamento sia stato chiamato
        self.mock_payment_processor.process_payment.assert_called_once()
        
        # Verifichiamo che il carrello non sia stato svuotato (l'operazione è fallita)
        self.assertEqual(self.cart.get_item_count(), 1)
    
    def test_place_order_success(self):
        """Verifica che place_order funzioni correttamente in caso di successo."""
        # Aggiungiamo alcuni prodotti al carrello
        self.cart.add_product(self.product1, 1)
        self.cart.add_product(self.product2, 2)
        
        # Calcoliamo il totale atteso
        expected_total = self.cart.get_total()
        
        # Configuriamo il mock per simulare un successo di pagamento
        self.mock_payment_processor.process_payment.return_value = {
            "success": True,
            "transaction_id": "txn_123456",
            "amount": expected_total,
            "timestamp": 1234567890
        }
        
        # Eseguiamo l'ordine
        order = self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
        
        # Verifichiamo che il processo di pagamento sia stato chiamato con i parametri corretti
        self.mock_payment_processor.process_payment.assert_called_once_with(expected_total, self.valid_payment_details)
        
        # Verifichiamo che l'ordine sia stato creato correttamente
        self.assertIn("order_id", order)
        self.assertEqual(order["user_details"], self.valid_user_details)
        self.assertEqual(len(order["items"]), 2)
        self.assertEqual(order["total_amount"], expected_total)
        self.assertEqual(order["payment"]["transaction_id"], "txn_123456")
        self.assertEqual(order["status"], "completed")
        
        # Verifichiamo che l'ordine sia stato aggiunto alla lista degli ordini
        self.assertEqual(len(self.order_service.orders), 1)
        
        # Verifichiamo che il carrello sia stato svuotato
        self.assertEqual(self.cart.get_item_count(), 0)
        
        # Verifichiamo che gli stock dei prodotti siano stati ridotti
        self.assertEqual(self.product1.stock, 4)  # 5 - 1
        self.assertEqual(self.product2.stock, 18)  # 20 - 2
    
    def test_get_order_existing(self):
        """Verifica che get_order restituisca un ordine esistente."""
        # Aggiungiamo un prodotto al carrello
        self.cart.add_product(self.product1, 1)
        
        # Configuriamo il mock per simulare un successo di pagamento
        self.mock_payment_processor.process_payment.return_value = {
            "success": True,
            "transaction_id": "txn_123456",
            "amount": self.cart.get_total(),
            "timestamp": 1234567890
        }
        
        # Creiamo un ordine
        order = self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
        order_id = order["order_id"]
        
        # Recuperiamo l'ordine
        retrieved_order = self.order_service.get_order(order_id)
        
        # Verifichiamo che l'ordine sia stato recuperato correttamente
        self.assertEqual(retrieved_order, order)
    
    def test_get_order_nonexistent(self):
        """Verifica che get_order restituisca None per un ordine inesistente."""
        retrieved_order = self.order_service.get_order("ordine-inesistente")
        self.assertIsNone(retrieved_order)
    
    def test_cancel_order_success(self):
        """Verifica che cancel_order funzioni correttamente in caso di successo."""
        # Aggiungiamo un prodotto al carrello
        self.cart.add_product(self.product1, 1)
        
        # Configuriamo il mock per simulare un successo di pagamento
        self.mock_payment_processor.process_payment.return_value = {
            "success": True,
            "transaction_id": "txn_123456",
            "amount": self.cart.get_total(),
            "timestamp": 1234567890
        }
        
        # Configuriamo il mock per simulare un successo di rimborso
        self.mock_payment_processor.refund_payment.return_value = {
            "success": True,
            "refund_id": "ref_123456",
            "transaction_id": "txn_123456",
            "timestamp": 1234567890
        }
        
        # Creiamo un ordine
        order = self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
        order_id = order["order_id"]
        
        # Annulliamo l'ordine
        result = self.order_service.cancel_order(order_id)
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        
        # Verifichiamo che il rimborso sia stato elaborato
        self.mock_payment_processor.refund_payment.assert_called_once_with("txn_123456")
        
        # Verifichiamo che lo stato dell'ordine sia stato aggiornato
        order = self.order_service.get_order(order_id)
        self.assertEqual(order["status"], "cancelled")
        self.assertIn("refund", order)
        self.assertEqual(order["refund"]["refund_id"], "ref_123456")
    
    def test_cancel_order_nonexistent(self):
        """Verifica che cancel_order sollevi un'eccezione per un ordine inesistente."""
        with self.assertRaises(ValueError):
            self.order_service.cancel_order("ordine-inesistente")
    
    def test_cancel_order_already_cancelled(self):
        """Verifica che cancel_order sollevi un'eccezione per un ordine già annullato."""
        # Aggiungiamo un prodotto al carrello
        self.cart.add_product(self.product1, 1)
        
        # Configuriamo i mock per simulare successo di pagamento e rimborso
        self.mock_payment_processor.process_payment.return_value = {
            "success": True,
            "transaction_id": "txn_123456",
            "amount": self.cart.get_total(),
            "timestamp": 1234567890
        }
        
        self.mock_payment_processor.refund_payment.return_value = {
            "success": True,
            "refund_id": "ref_123456",
            "transaction_id": "txn_123456",
            "timestamp": 1234567890
        }
        
        # Creiamo un ordine
        order = self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
        order_id = order["order_id"]
        
        # Annulliamo l'ordine
        self.order_service.cancel_order(order_id)
        
        # Proviamo ad annullare l'ordine di nuovo
        with self.assertRaises(RuntimeError):
            self.order_service.cancel_order(order_id)
    
    def test_cancel_order_refund_failure(self):
        """Verifica che cancel_order sollevi un'eccezione se il rimborso fallisce."""
        # Aggiungiamo un prodotto al carrello
        self.cart.add_product(self.product1, 1)
        
        # Configuriamo il mock per simulare un successo di pagamento
        self.mock_payment_processor.process_payment.return_value = {
            "success": True,
            "transaction_id": "txn_123456",
            "amount": self.cart.get_total(),
            "timestamp": 1234567890
        }
        
        # Configuriamo il mock per simulare un fallimento di rimborso
        self.mock_payment_processor.refund_payment.side_effect = RuntimeError("Rimborso fallito: impossibile elaborare la richiesta")
        
        # Creiamo un ordine
        order = self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
        order_id = order["order_id"]
        
        # Verifichiamo che venga sollevata un'eccezione
        with self.assertRaises(RuntimeError):
            self.order_service.cancel_order(order_id)
        
        # Verifichiamo che il rimborso sia stato tentato
        self.mock_payment_processor.refund_payment.assert_called_once_with("txn_123456")
        
        # Verifichiamo che lo stato dell'ordine non sia stato aggiornato
        order = self.order_service.get_order(order_id)
        self.assertEqual(order["status"], "completed")
        self.assertNotIn("refund", order)


class TestOrderServiceIntegration(unittest.TestCase):
    """Test di integrazione per OrderService che utilizza PaymentProcessor reale."""
    
    def setUp(self):
        """Inizializza un servizio ordini con un processore reale."""
        # Creiamo un processore di pagamenti reale (ma con patch per controllarne il comportamento)
        self.payment_processor = PaymentProcessor(api_key="test_api_key")
        
        # Creiamo un servizio ordini con il processore reale
        self.order_service = OrderService(self.payment_processor)
        
        # Creiamo un carrello
        self.cart = ShoppingCart()
        
        # Creiamo alcuni prodotti
        self.product1 = Product("p1", "Laptop", 999.99, 5)
        self.product2 = Product("p2", "Mouse", 29.99, 20)
        
        # Dettagli utente e pagamento validi
        self.valid_user_details = {
            "name": "Mario Rossi",
            "email": "mario.rossi@example.com",
            "address": "Via Roma 123, Milano"
        }
        
        self.valid_payment_details = {
            "card_number": "4111111111111111",
            "expiry": "12/25",
            "cvv": "123"
        }
    
    @patch('time.sleep')  # Mock per evitare il ritardo durante i test
    @patch('random.random')  # Mock per controllare la simulazione di successo/fallimento
    def test_complete_order_workflow(self, mock_random, mock_sleep):
        """Verifica un flusso di lavoro completo di ordine e annullamento."""
        # Impostiamo i mock per simulare sempre un successo
        mock_random.return_value = 0.5  # Valori per il successo
        mock_sleep.return_value = None  # Evita di attendere durante i test
        
        # Aggiungiamo prodotti al carrello
        self.cart.add_product(self.product1, 1)
        self.cart.add_product(self.product2, 2)
        
        initial_stock_p1 = self.product1.stock
        initial_stock_p2 = self.product2.stock
        
        # Applichiamo uno sconto
        self.cart.apply_discount(10)
        
        # Calcoliamo il totale atteso
        expected_total = self.cart.get_total()
        
        # Effettuiamo l'ordine
        order = self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
        order_id = order["order_id"]
        
        # Verifichiamo che l'ordine sia stato creato correttamente
        self.assertEqual(order["total_amount"], expected_total)
        self.assertEqual(order["status"], "completed")
        
        # Verifichiamo che il carrello sia stato svuotato
        self.assertEqual(self.cart.get_item_count(), 0)
        
        # Verifichiamo che gli stock siano stati ridotti
        self.assertEqual(self.product1.stock, initial_stock_p1 - 1)
        self.assertEqual(self.product2.stock, initial_stock_p2 - 2)
        
        # Verifichiamo che possiamo recuperare l'ordine
        retrieved_order = self.order_service.get_order(order_id)
        self.assertEqual(retrieved_order, order)
        
        # Annulliamo l'ordine
        self.order_service.cancel_order(order_id)
        
        # Verifichiamo che lo stato dell'ordine sia stato aggiornato
        cancelled_order = self.order_service.get_order(order_id)
        self.assertEqual(cancelled_order["status"], "cancelled")
        self.assertIn("refund", cancelled_order)
    
    @patch('time.sleep')  # Mock per evitare il ritardo durante i test
    @patch('random.random')  # Mock per controllare la simulazione di successo/fallimento
    def test_failed_payment_workflow(self, mock_random, mock_sleep):
        """Verifica un flusso di lavoro con pagamento fallito."""
        # Impostiamo il pagamento per fallire
        mock_sleep.return_value = None  # Evita di attendere durante i test
        
        # La prima chiamata a random è per il pagamento (deve fallire)
        # La seconda chiamata sarebbe per il rimborso (non dovremmo arrivare a questo punto)
        mock_random.side_effect = [0.95, 0.5]  # 0.95 > 0.9, quindi fallimento
        
        # Aggiungiamo un prodotto al carrello
        self.cart.add_product(self.product1, 1)
        
        initial_stock = self.product1.stock
        
        # Verifichiamo che venga sollevata un'eccezione
        with self.assertRaises(RuntimeError):
            self.order_service.place_order(self.cart, self.valid_user_details, self.valid_payment_details)
        
        # Verifichiamo che il carrello non sia stato svuotato
        self.assertEqual(self.cart.get_item_count(), 1)
        
        # Verifichiamo che lo stock non sia stato ridotto
        self.assertEqual(self.product1.stock, initial_stock)
        
        # Verifichiamo che non sia stato creato nessun ordine
        self.assertEqual(len(self.order_service.orders), 0)


if __name__ == '__main__':
    unittest.main()
