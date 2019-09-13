from Item import Item
from Specials import Special_N_M_X, CountSpecial_N_for_X


class Checkout:
    def __init__(self):
        # Database holding available items to purchase
        self.item_db = {}

        # checkout cart
        self.cart = {}

        # Markdowns
        self.markdowns = {}

        # Specials
        self.specials = {}

    def create_item_db_weight(self, name, cost):
        # If there's already an item with that name, it's an error
        if name in self.item_db:
            raise Exception

        self.item_db[name] = Item(name, cost, Item.TypeEnum.WEIGHT)

    def create_item_db_count(self, name, cost):
        # If there's already an item with that name, it's an error
        if name in self.item_db:
            raise Exception

        self.item_db[name] = Item(name, cost, Item.TypeEnum.COUNT)

    def get_item_cost(self, name):
        if name not in self.item_db:
            return None
        else:
            return self.item_db[name].get_cost()

    def remove_item_db(self, name):
        if name in self.item_db:
            del self.item_db[name]

    def scan(self, item_name, weight_amount=None):
        if item_name not in self.item_db:
            raise Exception

        if weight_amount is None:
            if self.item_db[item_name].get_type() is not Item.TypeEnum.COUNT:
                raise Exception
            # scanning an item by count
            if item_name not in self.cart:
                self.cart[item_name] = 1
            else:
                self.cart[item_name] += 1
        else:
            if self.item_db[item_name].get_type() is not Item.TypeEnum.WEIGHT:
                raise Exception

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

    def empty_cart(self):
        self.cart = {}

    def get_cart_total(self):
        cost = 0
        for item_name, unit_amount in self.cart.items():
            if item_name in self.specials:
                cost = cost + self._get_specials_cost(item_name, unit_amount)
            elif item_name in self.markdowns:
                cost = cost + self._get_markdown_cost(item_name, unit_amount)
            else:
                cost = cost + self._get_normal_cost(item_name, unit_amount)
        return cost

    def is_item_in_cart(self, name):
        item_cart = (True, self.cart[name]) if name in self.cart else (False, None)
        return item_cart

    def _get_normal_cost(self, name, amount):
        return self.item_db[name].get_cost() * amount

    def _get_markdown_cost(self, name, amount):
        return (self.item_db[name].get_cost() - self.markdowns[name]) * amount

    def _get_specials_cost(self, name, amount):
        cost = 0
        # compute the price of the items and also return whether there's an amount remaining
        # that the special wasn't applied to because of some limit
        special_cost, remaining_amount = self.specials[name].get_cost(amount)
        cost = cost + special_cost

        if remaining_amount > 0:
            if name in self.markdowns:
                cost += self._get_markdown_cost(name, remaining_amount)
            else:
                cost += self._get_normal_cost(name, remaining_amount)

        return cost

    def add_markdown(self, name, amount):
        self.markdowns[name] = amount

    def remove_markdown(self, name):
        if name in self.markdowns:
            del self.markdowns[name]

    def empty_markdowns(self):
        if self.markdowns:
            self.markdowns = {}

    def get_markdown(self, name):
        if name in self.markdowns:
            return self.markdowns[name]
        else:
            return None

    def add_special_N_M_X(self, name, N, M, X, limit=None):
        if name in self.item_db:
            unit_cost = self.item_db[name].get_cost()
            self.specials[name] = Special_N_M_X(unit_cost, N, M, X, limit)
        else:
            raise Exception

    def add_count_special_N_for_X(self, name, N, X, limit=None):
        if name in self.item_db and self.item_db[name].get_type() is Item.TypeEnum.COUNT:
            self.specials[name] = CountSpecial_N_for_X(N, X, limit)
        else:
            raise Exception


