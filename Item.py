from enum import Enum


class Item:

    class TypeEnum(Enum):
        WEIGHT = 1
        COUNT = 2

    def __init__(self, name, cost, item_type):
        self.name = name
        self.cost = cost
        self.type = item_type

    def get_type(self):
        return self.type

    def get_cost(self):
        return self.cost
