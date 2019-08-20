class Checkout:

    def __init__(self):
        self.item_weight_db = {}
        self.item_count_db = {}

    def createItemWeight(self, name, cost):
        self.item_weight_db[name] = cost

    def getItemCost(self, name):
        cost = self.item_weight_db[name] or self.item_count_db[name]
        if not cost:
            raise Exception
        return cost
