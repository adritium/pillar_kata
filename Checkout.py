from Item import Item

class Checkout:



    def __init__(self):
        # Database holding available items to purchase
        self.item_db = {}

        # Checkout cart
        self.cart = {}

    def createItemWeight(self, name, cost):
        self.item_db[name] = Item(name, cost, Item.ItemType.WEIGHT)

    def createItemCount(self, name, cost):
        self.item_db[name] = Item(name, cost, Item.ItemType.COUNT)

    def getItemCost(self, name):
        item = self.item_db[name]
        if not item:
            raise Exception
        return item.getCost()

    def removeItem(self, name):
        if name in self.item_db:
            del self.item_db[name]

    #def scanItem(self, name, count):




