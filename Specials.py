import math


class Special:
    def __init__(self):
        pass

    def get_cost(self, amount):
        pass


class Special_N_M_X(Special):
    # * "Buy num_full_price items get num_discounted at %percent_discounted off." For example, "Buy 1 get 1 free" or "Buy 2 get 1 half off."
    def __init__(self, unit_cost, num_full_price, num_discounted, percent_discounted, limit=None):
        self.num_full_price = num_full_price
        self.num_discounted = num_discounted
        self.percent_discounted = percent_discounted
        self.limit = limit
        self.unit_cost = unit_cost

    def get_cost(self, amount):
        # in case the special only applies to some of the items due to a limit
        effective_amount = amount
        if self.limit and self.limit < amount:
            effective_amount = self.limit

        remainder = effective_amount % (self.num_full_price + self.num_discounted)
        divisor = math.floor(effective_amount / (self.num_full_price + self.num_discounted))

        # number of items to which the full price applies
        num_full_price = divisor * self.num_full_price
        num_full_price += self.num_full_price if remainder > self.num_full_price else remainder

        # number of items left over
        num_discounted = divisor * self.num_discounted
        num_discounted += 0 if remainder < self.num_full_price else remainder - self.num_full_price

        cost = self.unit_cost * (num_full_price + (1 - self.percent_discounted / 100) * num_discounted)

        return cost, amount-effective_amount


class CountSpecial_N_for_X(Special):
    # * "num_full_price for $percent_discounted. in multiples of num_full_price" For example, "3 for $5.00"
    def __init__(self, num_items, price_for_num_items, limit=None):
        self.num_items = num_items
        self.price_for_num_items = price_for_num_items
        self.limit = limit

    def get_cost(self, amount):
        # in case the special only applies to some of the items due to a limit
        effective_amount = amount
        if self.limit and self.limit < amount:
            effective_amount = self.limit

        remainder = effective_amount % self.num_items
        effective_amount -= remainder

        cost = self.price_for_num_items / self.num_items * effective_amount

        return cost, (amount - effective_amount)
