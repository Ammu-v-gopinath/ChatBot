#source code
import re
from typing import List, Dict

#product in the store
class Product:
    def __init__(self, name: str, description: str, price: float, available: bool = True):
        self.name = name
        self.description = description
        self.price = price
        self.available = available

class ShoppingCart:
    def __init__(self):
        self.items: Dict[Product, int] = {}# Dictionary to store products and their quantities
        
    def add_item(self, product: Product, quantity: int = 1):
        if product in self.items:
            self.items[product] += quantity# Increment quantity if product already in cart
        else:
            self.items[product] = quantity # Add new product to cart
            
    def get_total(self) -> float:
        return sum(product.price * quantity for product, quantity in self.items.items()) #To calculates the total price of items in the cart
    
    def display(self) -> str:
        if not self.items:
            return "Your cart is empty."
        
        cart_display = "Your cart:\n"
        for product, quantity in self.items.items():
            cart_display += f"- {product.name} (x{quantity}): ${product.price * quantity:.2f}\n"
        cart_display += f"\nTotal: ${self.get_total():.2f}"
        return cart_display

    def clear_cart(self):
        self.items.clear()# Clears all items from the cart

class SalesChatbot:

    def __init__(self):#products available in the store
        self.products = [
            Product("Wireless Earbuds", "Bluetooth earbuds with noise cancellation", 59.99),
            Product("Portable Charger", "10000mAh portable charger with fast charging", 29.99),
            Product("Smart Home Camera", "1080p HD security camera with night vision", 89.99),
            Product("Electric Toothbrush", "Rechargeable toothbrush with multiple modes", 39.99),
            Product("Fitness Tracker", "Water-resistant tracker with heart rate monitor", 49.99),
        ]
        self.cart = ShoppingCart()

        
    def process_input(self, user_input: str) -> str:
        user_input = user_input.lower()
        
        if any(greeting in user_input for greeting in ["hello", "hi", "hey"]):
            return "Hello! Welcome to our virtual store. How can I help you today?"
        
        if any(phrase in user_input for phrase in ["what products", "show products", "list products"]):
            return self.list_products()
        
        if "tell me about" in user_input or "information about" in user_input:
            return self.get_product_info(user_input)
        
        if "recommend" in user_input:
            return self.recommend_product()
        
        if any(cart_phrase in user_input for cart_phrase in ["show cart", "view cart", "my cart"]):
            return self.cart.display()
        
        if "add" in user_input and any(product.name.lower() in user_input for product in self.products):
            return self.add_to_cart(user_input)
        
        if any(purchase_phrase in user_input for purchase_phrase in ["checkout", "complete purchase", "buy"]):
            return self.complete_purchase()
        
        return self.help_message()

    def list_products(self) -> str:
        products_list = "Here are our available products:\n"
        for product in self.products:
            status = "Available" if product.available else "Out of stock"
            products_list += f"- {product.name}: ${product.price:.2f} ({status})\n"
        return products_list

    def get_product_info(self, query: str) -> str:
        for product in self.products:
            if product.name.lower() in query:
                return f"{product.name}: {product.description}\nPrice: ${product.price:.2f}"
        return "I couldn't find information about that product."

    def recommend_product(self) -> str:
        recommended = max(self.products, key=lambda p: p.price)
        return f"I recommend our {recommended.name}! {recommended.description}\nPrice: ${recommended.price:.2f}"

    def add_to_cart(self, query: str) -> str:
        for product in self.products:
            if re.search(rf"\b{product.name.lower()}\b", query):
                if not product.available:
                    return f"Sorry, {product.name} is currently out of stock."
                
                quantity = 1
                quantity_match = re.search(r'(\d+)', query)
                if quantity_match:
                    quantity = int(quantity_match.group(1))
                
                self.cart.add_item(product, quantity)
                return f"Added {quantity} {product.name}(s) to your cart.\n" + self.cart.display()
        return "I couldn't find that product."

    def complete_purchase(self) -> str:
        if not self.cart.items:
            return "Your cart is empty. Add some products before checking out!"
        
        total = self.cart.get_total()
        self.cart.clear_cart()
        return f"Thank you for your purchase! Your total was ${total:.2f}. Your order will be processed shortly."

    def help_message(self) -> str:#To display commands for the user
        return """Here are some commands you can use:
        - "show products" to list available products
        - "tell me about <product_name>" for product details
        - "add <quantity> <product_name>" to add to cart
        - "show cart" to view your cart
        - "checkout" to complete the purchase
        - "exit" to quit the chatbot
        """

def main():# Main function to run the chatbot in a loop
    chatbot = SalesChatbot()
    print("Sales Chatbot: Hello! Welcome to our virtual store. How can I help you today?")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Sales Chatbot: Thank you for shopping with us. Goodbye!")
            break
            
        response = chatbot.process_input(user_input)
        print("Sales Chatbot:", response)

if __name__ == "__main__":
    main()
