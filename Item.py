from enum import Enum

class Item:

    class ItemType(Enum):
        WEIGHT = 1
        COUNT = 2

    def __init__(self, name, cost, item_type):
        self.name = name
        self.cost = cost
        self.type = item_type

    def getType(self):
        return self.type

    def getCost(self):
        return self.cost
