from Item import Item


class Checkout:
    def __init__(self):
        # Database holding available items to purchase
        self.item_db = {}

        # Checkout cart
        self.cart = {}

    def create_item_db_weight(self, name, cost):
        # If there's already an item with that name, it's an error
        if name in self.item_db:
            raise Exception

        self.item_db[name] = Item(name, cost, Item.ItemType.WEIGHT)

    def create_item_db_count(self, name, cost):
        # If there's already an item with that name, it's an error
        if name in self.item_db:
            raise Exception

        self.item_db[name] = Item(name, cost, Item.ItemType.COUNT)

    def get_item_cost(self, name):
        item = self.item_db[name]
        if not item:
            raise Exception
        return item.get_cost()

    def remove_item_db(self, name):
        if name in self.item_db:
            del self.item_db[name]

    def scan(self, item_name, weight_amount=None):
        if weight_amount is None:
            # scanning an item by count
            if item_name not in self.cart:
                self.cart[item_name] = 1
            else:
                self.cart[item_name] += 1
        else:
            if item_name not in self.cart:
                self.cart[item_name] = weight_amount
            else:
                self.cart[item_name] += weight_amount

    def unscan(self, name, weight_amount=None):
        if name not in self.cart:
            raise Exception

        if weight_amount is None:
            # removing an instance of an item by count
            self.cart[name] -= 1
        else:
            self.cart[name] -= weight_amount

        if self.cart[name] == 0:
            del self.cart[name]

    def get_cart_total(self):
        cost = 0
        for item_name, unit_amount in self.cart.items():
            cost = cost + self.get_item_cost(item_name) * unit_amount
        return cost

    def is_item_in_cart(self, name):
        item_cart = (True, self.cart[name]) if name in self.cart else (False, None)
        return item_cart

