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

    def remove_item(self, name):
        if name in self.item_db:
            del self.item_db[name]

    #def scanItem(self, name, count):




