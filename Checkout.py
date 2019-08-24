from Item import Item


class Checkout:
    def __init__(self):
        # Database holding available items to purchase
        self.item_db = {}

        # Checkout cart
        self.cart = {}

    def create_item_db_weight(self, name, cost):
        self.item_db[name] = Item(name, cost, Item.ItemType.WEIGHT)

    def create_item_db_count(self, name, cost):
        self.item_db[name] = Item(name, cost, Item.ItemType.COUNT)

    def get_item_cost(self, name):
        item = self.item_db[name]
        if not item:
            raise Exception
        return item.get_cost()

    def remove_item_db(self, name):
        if name in self.item_db:
            del self.item_db[name]

    def encart(self, item_name, unit_amount):
        self.cart[item_name] = unit_amount

    def get_cart_total(self):
        cost = 0
        for item_name, unit_amount in self.cart.items():
            cost = cost + self.get_item_cost(item_name) * unit_amount
        return cost

    #def scanItem(self, name, count):




