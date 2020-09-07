from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):

    def __init__(self, request):
        # Initialize the cart
        self.session = request.session
        # request.session is the inbuilt method to get the current session
        cart = self.session.get(session.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session in the dictionary(in JSON format)
            cart = self.session[settings.CART_SESSION_ID] = {}
        # if the cart exists then get the original instance of the cart from the session
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        # Add a product to the cart or update its quantity
        product_id = str(product.id)
        if product_id not in self.cart:
            # If product doesn't exist in the cart at-all then add it
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            # If we want to increase or decrease the quantity of the product in the cart
            self.cart[product_id]['quantity'] = quantity
        else:
            # If we have added a new product in the cart, then by default quantity is 1
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified  = True

    def remove(self, product):
        # Remove a product from the cart
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        # Iterate over the items in the cart and get the products from the db
        product_ids = self.cart.keys()
        # Get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        # We copy the original cart into a new cart
        for product in products:
            # We add a new field called 'product' and copy all product instances into the new cart
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            # We convert all prices from string to Decimal
            # Below we add a new attribute called "total_price" to the cart
            item['total_price'] = item['price'] * item['quantity']
            # We calculate the total price with the prices of the product at that instances
            yield item
            # yield is called to return from a function something without destroying the local variables in the function

    def __len__(self):
        # Count all items in the cart
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Remove the cart from the session
        del self.session[settings.CART_SESSION_ID]
        self.save()