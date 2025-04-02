"""
Sistema di carrello per acquisti online
"""
from typing import Dict, List, Optional, Tuple
import time
import random


class Product:
    """Rappresenta un prodotto acquistabile."""
    
    def __init__(self, product_id: str, name: str, price: float, stock: int = 10):
        """Inizializza un nuovo prodotto."""
        if price <= 0:
            raise ValueError("Il prezzo deve essere maggiore di zero")
        if stock < 0:
            raise ValueError("La disponibilità non può essere negativa")
        
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
    
    def is_available(self, quantity: int = 1) -> bool:
        """
        Verifica se il prodotto è disponibile nella quantità richiesta.
        
        Args:
            quantity: La quantità richiesta
            
        Returns:
            bool: True se il prodotto è disponibile nella quantità richiesta
        """
        return self.stock >= quantity
    
    def reserve(self, quantity: int = 1) -> bool:
        """
        Riserva una quantità del prodotto (riduce lo stock).
        
        Args:
            quantity: La quantità da riservare
            
        Returns:
            bool: True se la riserva è andata a buon fine
            
        Raises:
            ValueError: Se la quantità richiesta non è disponibile
        """
        if not self.is_available(quantity):
            raise ValueError(f"Quantità non disponibile per {self.name}")
        
        self.stock -= quantity
        return True
    
    def restock(self, quantity: int) -> int:
        """
        Incrementa lo stock del prodotto.
        
        Args:
            quantity: La quantità da aggiungere allo stock
            
        Returns:
            int: Il nuovo livello di stock
            
        Raises:
            ValueError: Se la quantità è negativa
        """
        if quantity < 0:
            raise ValueError("La quantità di restock deve essere positiva")
        
        self.stock += quantity
        return self.stock


class ShoppingCart:
    """Gestisce un carrello della spesa."""
    
    def __init__(self):
        """Inizializza un nuovo carrello vuoto."""
        self.items: Dict[str, Tuple[Product, int]] = {}  # product_id -> (product, quantity)
        self.discount_percent = 0
    
    def add_product(self, product: Product, quantity: int = 1) -> bool:
        """
        Aggiunge un prodotto al carrello.
        
        Args:
            product: Il prodotto da aggiungere
            quantity: La quantità da aggiungere
            
        Returns:
            bool: True se il prodotto è stato aggiunto con successo
            
        Raises:
            ValueError: Se la quantità è negativa o zero
            ValueError: Se il prodotto non è disponibile nella quantità richiesta
        """
        if quantity <= 0:
            raise ValueError("La quantità deve essere positiva")
        
        if not product.is_available(quantity):
            raise ValueError(f"Quantità {quantity} non disponibile per {product.name}")
        
        if product.product_id in self.items:
            current_product, current_quantity = self.items[product.product_id]
            self.items[product.product_id] = (current_product, current_quantity + quantity)
        else:
            self.items[product.product_id] = (product, quantity)
        
        return True
    
    def remove_product(self, product_id: str, quantity: int = 1) -> bool:
        """
        Rimuove un prodotto dal carrello.
        
        Args:
            product_id: L'ID del prodotto da rimuovere
            quantity: La quantità da rimuovere
            
        Returns:
            bool: True se il prodotto è stato rimosso con successo
            
        Raises:
            ValueError: Se il prodotto non è nel carrello
            ValueError: Se la quantità è maggiore di quella nel carrello
        """
        if product_id not in self.items:
            raise ValueError(f"Prodotto con ID {product_id} non presente nel carrello")
        
        current_product, current_quantity = self.items[product_id]
        
        if quantity <= 0:
            raise ValueError("La quantità da rimuovere deve essere positiva")
        
        if quantity > current_quantity:
            raise ValueError(f"Quantità da rimuovere ({quantity}) maggiore di quella nel carrello ({current_quantity})")
        
        if quantity == current_quantity:
            # Rimuovi completamente il prodotto
            del self.items[product_id]
        else:
            # Riduci la quantità
            self.items[product_id] = (current_product, current_quantity - quantity)
        
        return True
    
    def get_total(self) -> float:
        """
        Calcola il totale del carrello.
        
        Returns:
            float: Il totale del carrello
        """
        total = sum(product.price * quantity for product, quantity in self.items.values())
        
        # Applica lo sconto se presente
        if self.discount_percent > 0:
            total = total * (1 - self.discount_percent / 100)
        
        return round(total, 2)
    
    def apply_discount(self, percent: float) -> bool:
        """
        Applica uno sconto percentuale al carrello.
        
        Args:
            percent: La percentuale di sconto (0-100)
            
        Returns:
            bool: True se lo sconto è stato applicato con successo
            
        Raises:
            ValueError: Se la percentuale non è valida
        """
        if percent < 0 or percent > 100:
            raise ValueError("La percentuale di sconto deve essere compresa tra 0 e 100")
        
        self.discount_percent = percent
        return True
    
    def clear(self) -> bool:
        """
        Svuota il carrello.
        
        Returns:
            bool: True se il carrello è stato svuotato con successo
        """
        self.items.clear()
        self.discount_percent = 0
        return True
    
    def get_item_count(self) -> int:
        """
        Ottiene il numero totale di articoli nel carrello.
        
        Returns:
            int: Il numero totale di articoli
        """
        return sum(quantity for _, quantity in self.items.values())
    
    def checkout(self) -> List[Tuple[Product, int]]:
        """
        Prepara il checkout del carrello.
        
        Returns:
            List[Tuple[Product, int]]: Lista di prodotti e quantità
            
        Raises:
            ValueError: Se il carrello è vuoto
        """
        if not self.items:
            raise ValueError("Impossibile completare il checkout: il carrello è vuoto")
        
        # Verifica che tutti i prodotti siano ancora disponibili
        for product, quantity in self.items.values():
            if not product.is_available(quantity):
                raise ValueError(f"Prodotto {product.name} non più disponibile nella quantità richiesta")
        
        # Crea la lista di checkout
        checkout_list = [(product, quantity) for product, quantity in self.items.values()]
        
        return checkout_list


class PaymentProcessor:
    """Gestisce l'elaborazione dei pagamenti."""
    
    def __init__(self, api_key: str = "test_key"):
        """
        Inizializza un nuovo processore di pagamenti.
        
        Args:
            api_key: La chiave API per il servizio di pagamento
        """
        self.api_key = api_key
    
    def process_payment(self, amount: float, payment_details: Dict) -> Dict:
        """
        Elabora un pagamento.
        
        Args:
            amount: L'importo da pagare
            payment_details: I dettagli del pagamento
            
        Returns:
            Dict: Risultato del pagamento
            
        Raises:
            ValueError: Se i dettagli di pagamento non sono validi
            RuntimeError: Se il pagamento fallisce
        """
        # Verifica che i dettagli di pagamento siano validi
        required_fields = ["card_number", "expiry", "cvv"]
        for field in required_fields:
            if field not in payment_details:
                raise ValueError(f"Campo obbligatorio mancante: {field}")
        
        # Simulazione di chiamata API a un servizio di pagamento
        # In un'implementazione reale, qui ci sarebbe una chiamata HTTP a un gateway di pagamento
        print(f"Elaborazione pagamento di €{amount:.2f}...")
        
        # Simulazione di latenza di rete
        time.sleep(0.5)
        
        # Simulazione di risposta (90% di successo, 10% di fallimento)
        if random.random() < 0.9:
            return {
                "success": True,
                "transaction_id": f"txn_{random.randint(100000, 999999)}",
                "amount": amount,
                "timestamp": time.time()
            }
        else:
            raise RuntimeError("Pagamento fallito: la transazione è stata rifiutata")
    
    def refund_payment(self, transaction_id: str) -> Dict:
        """
        Effettua il rimborso di un pagamento.
        
        Args:
            transaction_id: ID della transazione da rimborsare
            
        Returns:
            Dict: Risultato del rimborso
            
        Raises:
            ValueError: Se l'ID della transazione non è valido
            RuntimeError: Se il rimborso fallisce
        """
        if not transaction_id.startswith("txn_"):
            raise ValueError("ID transazione non valido")
        
        # Simulazione di chiamata API per il rimborso
        print(f"Elaborazione rimborso per la transazione {transaction_id}...")
        
        # Simulazione di latenza di rete
        time.sleep(0.5)
        
        # Simulazione di risposta (95% di successo, 5% di fallimento)
        if random.random() < 0.95:
            return {
                "success": True,
                "refund_id": f"ref_{random.randint(100000, 999999)}",
                "transaction_id": transaction_id,
                "timestamp": time.time()
            }
        else:
            raise RuntimeError("Rimborso fallito: impossibile elaborare la richiesta")


class OrderService:
    """Gestisce il processo di ordine completo."""
    
    def __init__(self, payment_processor: PaymentProcessor):
        """
        Inizializza un nuovo servizio ordini.
        
        Args:
            payment_processor: Il processore di pagamenti da utilizzare
        """
        self.payment_processor = payment_processor
        self.orders: List[Dict] = []
    
    def place_order(self, cart: ShoppingCart, user_details: Dict, payment_details: Dict) -> Dict:
        """
        Effettua un ordine.
        
        Args:
            cart: Il carrello della spesa
            user_details: Dettagli dell'utente
            payment_details: Dettagli del pagamento
            
        Returns:
            Dict: Dettagli dell'ordine completato
            
        Raises:
            ValueError: Se il carrello è vuoto o i dettagli non sono validi
            RuntimeError: Se il pagamento fallisce
        """
        # Verifica che il carrello non sia vuoto
        if cart.get_item_count() == 0:
            raise ValueError("Impossibile completare l'ordine: il carrello è vuoto")
        
        # Verifica che i dettagli dell'utente siano validi
        required_user_fields = ["name", "email", "address"]
        for field in required_user_fields:
            if field not in user_details:
                raise ValueError(f"Campo utente obbligatorio mancante: {field}")
        
        # Preparare il checkout
        checkout_items = cart.checkout()
        total_amount = cart.get_total()
        
        # Elabora il pagamento
        payment_result = self.payment_processor.process_payment(total_amount, payment_details)
        
        # Se il pagamento ha avuto successo, riduci lo stock e crea l'ordine
        if payment_result["success"]:
            # Riduci lo stock dei prodotti
            for product, quantity in checkout_items:
                product.reserve(quantity)
            
            # Crea l'ordine
            order = {
                "order_id": f"order_{len(self.orders) + 1}",
                "user_details": user_details,
                "items": [(product.name, quantity) for product, quantity in checkout_items],
                "total_amount": total_amount,
                "payment": payment_result,
                "status": "completed",
                "timestamp": time.time()
            }
            
            # Aggiungi l'ordine alla lista degli ordini
            self.orders.append(order)
            
            # Svuota il carrello
            cart.clear()
            
            return order
        else:
            # Non dovrebbe mai arrivare qui, poiché process_payment solleva un'eccezione in caso di fallimento
            raise RuntimeError("Pagamento fallito")
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """
        Ottiene i dettagli di un ordine.
        
        Args:
            order_id: L'ID dell'ordine
            
        Returns:
            Optional[Dict]: Dettagli dell'ordine o None se non trovato
        """
        for order in self.orders:
            if order["order_id"] == order_id:
                return order
        return None
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Annulla un ordine.
        
        Args:
            order_id: L'ID dell'ordine da annullare
            
        Returns:
            bool: True se l'ordine è stato annullato con successo
            
        Raises:
            ValueError: Se l'ordine non esiste
            RuntimeError: Se l'annullamento fallisce
        """
        # Trova l'ordine
        order = self.get_order(order_id)
        if not order:
            raise ValueError(f"Ordine con ID {order_id} non trovato")
        
        # Verifica che l'ordine non sia già stato annullato
        if order["status"] == "cancelled":
            raise RuntimeError("L'ordine è già stato annullato")
        
        # Effettua il rimborso
        refund_result = self.payment_processor.refund_payment(order["payment"]["transaction_id"])
        
        if refund_result["success"]:
            # Aggiorna lo stato dell'ordine
            order["status"] = "cancelled"
            order["refund"] = refund_result
            
            # In uno scenario reale, qui si potrebbe anche riaggiungere i prodotti allo stock
            return True
        else:
            # Non dovrebbe mai arrivare qui, poiché refund_payment solleva un'eccezione in caso di fallimento
            raise RuntimeError("Annullamento fallito")


# Esempio di utilizzo
if __name__ == "__main__":
    # Crea alcuni prodotti
    p1 = Product("p1", "Laptop", 999.99, 5)
    p2 = Product("p2", "Mouse", 29.99, 20)
    p3 = Product("p3", "Tastiera", 59.99, 15)
    
    # Crea un carrello
    cart = ShoppingCart()
    
    # Aggiungi prodotti al carrello
    cart.add_product(p1, 1)
    cart.add_product(p2, 2)
    cart.add_product(p3, 1)
    
    # Applica uno sconto
    cart.apply_discount(10)
    
    # Visualizza il totale
    print(f"Totale carrello: €{cart.get_total():.2f}")
    
    # Crea un processore di pagamenti
    payment_processor = PaymentProcessor(api_key="test_key")
    
    # Crea un servizio ordini
    order_service = OrderService(payment_processor)
    
    # Dettagli utente e pagamento
    user_details = {
        "name": "Mario Rossi",
        "email": "mario.rossi@example.com",
        "address": "Via Roma 123, Milano"
    }
    
    payment_details = {
        "card_number": "4111111111111111",
        "expiry": "12/23",
        "cvv": "123"
    }
    
    try:
        # Effettua l'ordine
        order = order_service.place_order(cart, user_details, payment_details)
        print(f"Ordine completato con ID: {order['order_id']}")
        
        # Annulla l'ordine
        order_service.cancel_order(order["order_id"])
        print("Ordine annullato con successo")
    except Exception as e:
        print(f"Errore: {e}")
