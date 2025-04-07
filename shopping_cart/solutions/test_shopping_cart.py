"""
Test unitari per la classe ShoppingCart
"""
import unittest
from main import ShoppingCart, Product


class TestShoppingCart(unittest.TestCase):
    """Test per la classe ShoppingCart."""
    
    def setUp(self):
        """Inizializza un carrello e alcuni prodotti prima di ogni test."""
        # Creiamo un carrello vuoto
        self.cart = ShoppingCart()
        
        # Creiamo alcuni prodotti di esempio
        self.product1 = Product("p1", "Laptop", 999.99, 5)
        self.product2 = Product("p2", "Mouse", 29.99, 20)
        self.product3 = Product("p3", "Tastiera", 59.99, 15)
    
    def test_init(self):
        """Verifica che l'inizializzazione del carrello funzioni correttamente."""
        self.assertEqual(len(self.cart.items), 0)  # Il carrello dovrebbe iniziare vuoto
        self.assertEqual(self.cart.discount_percent, 0)  # Nessuno sconto iniziale
    
    def test_add_product_success(self):
        """Verifica che l'aggiunta di un prodotto funzioni correttamente."""
        # Aggiungiamo un prodotto
        result = self.cart.add_product(self.product1, 2)
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        
        # Verifichiamo che il prodotto sia stato aggiunto
        self.assertEqual(len(self.cart.items), 1)
        self.assertIn(self.product1.product_id, self.cart.items)
        
        # Verifichiamo che la quantità sia corretta
        product, quantity = self.cart.items[self.product1.product_id]
        self.assertEqual(product, self.product1)
        self.assertEqual(quantity, 2)
    
    def test_add_product_update_quantity(self):
        """Verifica che aggiungere un prodotto già presente aggiorni la quantità."""
        # Aggiungiamo un prodotto
        self.cart.add_product(self.product1, 2)
        
        # Aggiungiamo lo stesso prodotto di nuovo
        result = self.cart.add_product(self.product1, 1)
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        
        # Verifichiamo che ci sia ancora solo un elemento nel carrello
        self.assertEqual(len(self.cart.items), 1)
        
        # Verifichiamo che la quantità sia stata aggiornata
        product, quantity = self.cart.items[self.product1.product_id]
        self.assertEqual(quantity, 3)
    
    def test_add_product_invalid_quantity(self):
        """Verifica che aggiungere un prodotto con quantità non valida sollevi un'eccezione."""
        # Quantità zero
        with self.assertRaises(ValueError):
            self.cart.add_product(self.product1, 0)
        
        # Quantità negativa
        with self.assertRaises(ValueError):
            self.cart.add_product(self.product1, -1)
        
        # Verifichiamo che il carrello sia ancora vuoto
        self.assertEqual(len(self.cart.items), 0)
    
    def test_add_product_insufficient_stock(self):
        """Verifica che aggiungere un prodotto con stock insufficiente sollevi un'eccezione."""
        # Quantità superiore allo stock
        with self.assertRaises(ValueError):
            self.cart.add_product(self.product1, 6)  # Stock è 5
        
        # Verifichiamo che il carrello sia ancora vuoto
        self.assertEqual(len(self.cart.items), 0)
    
    def test_remove_product_success(self):
        """Verifica che la rimozione di un prodotto funzioni correttamente."""
        # Aggiungiamo un prodotto
        self.cart.add_product(self.product1, 3)
        
        # Rimuoviamo parte della quantità
        result = self.cart.remove_product(self.product1.product_id, 2)
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        
        # Verifichiamo che la quantità sia stata aggiornata
        product, quantity = self.cart.items[self.product1.product_id]
        self.assertEqual(quantity, 1)
        
        # Rimuoviamo il resto della quantità
        result = self.cart.remove_product(self.product1.product_id, 1)
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        
        # Verifichiamo che il prodotto sia stato completamente rimosso
        self.assertEqual(len(self.cart.items), 0)
    
    def test_remove_product_not_in_cart(self):
        """Verifica che rimuovere un prodotto non presente sollevi un'eccezione."""
        with self.assertRaises(ValueError):
            self.cart.remove_product("prodotto-inesistente")
    
    def test_remove_product_invalid_quantity(self):
        """Verifica che rimuovere un prodotto con quantità non valida sollevi un'eccezione."""
        # Aggiungiamo un prodotto
        self.cart.add_product(self.product1, 3)
        
        # Quantità zero
        with self.assertRaises(ValueError):
            self.cart.remove_product(self.product1.product_id, 0)
        
        # Quantità negativa
        with self.assertRaises(ValueError):
            self.cart.remove_product(self.product1.product_id, -1)
        
        # Quantità superiore a quella nel carrello
        with self.assertRaises(ValueError):
            self.cart.remove_product(self.product1.product_id, 4)
        
        # Verifichiamo che la quantità non sia cambiata
        product, quantity = self.cart.items[self.product1.product_id]
        self.assertEqual(quantity, 3)
    
    def test_get_total_empty_cart(self):
        """Verifica che get_total restituisca 0 per un carrello vuoto."""
        total = self.cart.get_total()
        self.assertEqual(total, 0)
    
    def test_get_total_without_discount(self):
        """Verifica che get_total calcoli correttamente il totale senza sconti."""
        # Aggiungiamo alcuni prodotti
        self.cart.add_product(self.product1, 2)  # 2 * 999.99 = 1999.98
        self.cart.add_product(self.product2, 1)  # 1 * 29.99 = 29.99
        
        # Calcoliamo il totale atteso
        expected_total = (2 * 999.99) + (1 * 29.99)
        
        # Verifichiamo che il totale sia corretto
        total = self.cart.get_total()
        self.assertEqual(total, round(expected_total, 2))
    
    def test_get_total_with_discount(self):
        """Verifica che get_total calcoli correttamente il totale con sconti."""
        # Aggiungiamo alcuni prodotti
        self.cart.add_product(self.product1, 1)  # 1 * 999.99 = 999.99
        self.cart.add_product(self.product2, 2)  # 2 * 29.99 = 59.98
        
        # Calcoliamo il totale senza sconto
        base_total = 999.99 + 59.98
        
        # Applichiamo uno sconto del 10%
        self.cart.apply_discount(10)
        
        # Calcoliamo il totale atteso con sconto
        expected_total = base_total * 0.9
        
        # Verifichiamo che il totale sia corretto
        total = self.cart.get_total()
        self.assertEqual(total, round(expected_total, 2))
    
    def test_apply_discount_success(self):
        """Verifica che apply_discount imposti correttamente lo sconto."""
        # Applichiamo uno sconto
        result = self.cart.apply_discount(15)
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        
        # Verifichiamo che lo sconto sia stato impostato
        self.assertEqual(self.cart.discount_percent, 15)
        
        # Applichiamo un altro sconto
        result = self.cart.apply_discount(20)
        
        # Verifichiamo che lo sconto sia stato aggiornato
        self.assertEqual(self.cart.discount_percent, 20)
    
    def test_apply_discount_invalid(self):
        """Verifica che apply_discount sollevi un'eccezione con percentuale non valida."""
        # Percentuale negativa
        with self.assertRaises(ValueError):
            self.cart.apply_discount(-5)
        
        # Percentuale superiore a 100
        with self.assertRaises(ValueError):
            self.cart.apply_discount(101)
        
        # Verifichiamo che lo sconto non sia cambiato
        self.assertEqual(self.cart.discount_percent, 0)
    
    def test_clear(self):
        """Verifica che clear svuoti correttamente il carrello."""
        # Aggiungiamo alcuni prodotti
        self.cart.add_product(self.product1, 1)
        self.cart.add_product(self.product2, 2)
        
        # Applichiamo uno sconto
        self.cart.apply_discount(10)
        
        # Verifichiamo che il carrello non sia vuoto
        self.assertNotEqual(len(self.cart.items), 0)
        self.assertNotEqual(self.cart.discount_percent, 0)
        
        # Svuotiamo il carrello
        result = self.cart.clear()
        
        # Verifichiamo che l'operazione abbia avuto successo
        self.assertTrue(result)
        
        # Verifichiamo che il carrello sia vuoto
        self.assertEqual(len(self.cart.items), 0)
        
        # Verifichiamo che lo sconto sia stato resettato
        self.assertEqual(self.cart.discount_percent, 0)
    
    def test_get_item_count(self):
        """Verifica che get_item_count restituisca il numero corretto di articoli."""
        # Carrello vuoto
        self.assertEqual(self.cart.get_item_count(), 0)
        
        # Aggiungiamo alcuni prodotti
        self.cart.add_product(self.product1, 2)
        self.cart.add_product(self.product2, 3)
        
        # Verifichiamo che il conteggio sia corretto
        self.assertEqual(self.cart.get_item_count(), 5)
        
        # Rimuoviamo un prodotto
        self.cart.remove_product(self.product1.product_id, 1)
        
        # Verifichiamo che il conteggio sia stato aggiornato
        self.assertEqual(self.cart.get_item_count(), 4)
    
    def test_checkout_success(self):
        """Verifica che checkout restituisca la lista corretta di prodotti."""
        # Aggiungiamo alcuni prodotti
        self.cart.add_product(self.product1, 2)
        self.cart.add_product(self.product2, 1)
        
        # Eseguiamo il checkout
        checkout_list = self.cart.checkout()
        
        # Verifichiamo che la lista contenga i prodotti corretti
        self.assertEqual(len(checkout_list), 2)
        
        # Verifichiamo che i prodotti e le quantità siano corretti
        for product, quantity in checkout_list:
            if product.product_id == "p1":
                self.assertEqual(quantity, 2)
            elif product.product_id == "p2":
                self.assertEqual(quantity, 1)
            else:
                self.fail(f"Prodotto non previsto nel checkout: {product.product_id}")
    
    def test_checkout_empty_cart(self):
        """Verifica che checkout sollevi un'eccezione con carrello vuoto."""
        with self.assertRaises(ValueError):
            self.cart.checkout()
    
    def test_checkout_stock_changed(self):
        """Verifica che checkout verifichi la disponibilità corrente dei prodotti."""
        # Aggiungiamo un prodotto
        self.cart.add_product(self.product1, 5)  # Tutto lo stock disponibile
        
        # Modifichiamo lo stock (simulando un acquisto da parte di un altro utente)
        self.product1.stock = 3
        
        # Il checkout dovrebbe fallire perché lo stock è cambiato
        with self.assertRaises(ValueError):
            self.cart.checkout()


if __name__ == '__main__':
    unittest.main()
