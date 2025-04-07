"""
Test unitari per la classe Product
"""
import unittest
from main import Product


class TestProduct(unittest.TestCase):
    """Test per la classe Product."""
    
    def setUp(self):
        """Inizializza un prodotto prima di ogni test."""
        # Creiamo un prodotto valido
        self.product = Product("p1", "Laptop", 999.99, 5)
    
    def test_init_valid(self):
        """Verifica che l'inizializzazione funzioni correttamente con parametri validi."""
        # Verifichiamo che gli attributi siano impostati correttamente
        self.assertEqual(self.product.product_id, "p1")
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.stock, 5)
    
    def test_init_invalid_price(self):
        """Verifica che l'inizializzazione sollevi un'eccezione con prezzo non valido."""
        # Prezzo zero
        with self.assertRaises(ValueError):
            Product("p2", "Mouse", 0, 10)
        
        # Prezzo negativo
        with self.assertRaises(ValueError):
            Product("p3", "Tastiera", -10.99, 10)
    
    def test_init_invalid_stock(self):
        """Verifica che l'inizializzazione sollevi un'eccezione con stock negativo."""
        with self.assertRaises(ValueError):
            Product("p4", "Monitor", 299.99, -1)
    
    def test_is_available_sufficient_stock(self):
        """Verifica che is_available restituisca True quando lo stock è sufficiente."""
        # Quantità esatta
        self.assertTrue(self.product.is_available(5))
        
        # Quantità inferiore
        self.assertTrue(self.product.is_available(3))
        
        # Quantità predefinita (1)
        self.assertTrue(self.product.is_available())
    
    def test_is_available_insufficient_stock(self):
        """Verifica che is_available restituisca False quando lo stock è insufficiente."""
        # Quantità superiore
        self.assertFalse(self.product.is_available(6))
        
        # Quantità molto superiore
        self.assertFalse(self.product.is_available(100))
    
    def test_reserve_success(self):
        """Verifica che reserve riduca correttamente lo stock quando la quantità è disponibile."""
        # Riserviamo 2 unità
        result = self.product.reserve(2)
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        # Verifichiamo che lo stock sia stato ridotto
        self.assertEqual(self.product.stock, 3)
        
        # Riserviamo altre 3 unità (tutte quelle rimanenti)
        result = self.product.reserve(3)
        self.assertTrue(result)
        self.assertEqual(self.product.stock, 0)
    
    def test_reserve_failure(self):
        """Verifica che reserve sollevi un'eccezione quando la quantità non è disponibile."""
        # Quantità superiore allo stock
        with self.assertRaises(ValueError):
            self.product.reserve(6)
        
        # Verifichiamo che lo stock non sia cambiato
        self.assertEqual(self.product.stock, 5)
        
        # Riserviamo tutto lo stock
        self.product.reserve(5)
        
        # Ora che lo stock è 0, anche una richiesta di 1 unità dovrebbe fallire
        with self.assertRaises(ValueError):
            self.product.reserve(1)
    
    def test_restock_success(self):
        """Verifica che restock aumenti correttamente lo stock."""
        # Aggiungiamo 10 unità allo stock
        new_stock = self.product.restock(10)
        
        # Verifichiamo che il nuovo stock sia corretto
        self.assertEqual(new_stock, 15)
        self.assertEqual(self.product.stock, 15)
        
        # Aggiungiamo 0 unità (operazione valida ma senza effetto)
        new_stock = self.product.restock(0)
        self.assertEqual(new_stock, 15)
    
    def test_restock_failure(self):
        """Verifica che restock sollevi un'eccezione con quantità negativa."""
        with self.assertRaises(ValueError):
            self.product.restock(-5)
        
        # Verifichiamo che lo stock non sia cambiato
        self.assertEqual(self.product.stock, 5)


if __name__ == '__main__':
    unittest.main()
