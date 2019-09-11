import math
class Special:
    def __init__(self):
        pass

    def get_cost(self, amount):
        pass


class CountSpecial_N_M_X(Special):
    # * "Buy N items get M at %X off." For example, "Buy 1 get 1 free" or "Buy 2 get 1 half off."
    def __init__(self, unit_cost, N, M, X, limit=None):
        self.N = N
        self.M = M
        self.X = X
        self.limit = limit
        self.unit_cost = unit_cost

    def get_cost(self, amount):
        # in case the special only applies to some of the items due to a limit
        effective_amount = amount
        if self.limit and self.limit < amount:
            effective_amount = self.limit

        remainder = effective_amount % (self.N + self.M)
        divisor = math.floor(effective_amount / (self.N + self.M))

        # number of items to which the full price applies
        num_full_price = divisor * self.N
        num_full_price += self.N if remainder > self.N else remainder

        # number of items left over
        num_discounted = divisor * self.M
        num_discounted += 0 if remainder < self.N else remainder - self.N

        cost = self.unit_cost * (num_full_price + (1-self.X/100)*num_discounted)

        return cost, amount-effective_amount


class CountSpecial_N_for_X(Special):
    # * "N for $X. in multiples of N" For example, "3 for $5.00"
    def __init__(self, N, X, limit=None):
        self.N = N
        self.X = X
        self.limit = limit

    def get_cost(self, amount):
        # in case the special only applies to some of the items due to a limit
        effective_amount = amount
        if self.limit and self.limit < amount:
            effective_amount = self.limit

        remainder = effective_amount % self.N
        effective_amount -= remainder

        cost = self.X/self.N * effective_amount

        return cost, (amount - effective_amount)


class WeightSpecial1(Special):
    # * "Buy N, get M of equal or lesser value for %X off"
    def __init__(self, unit_cost, N, M, X, limit=None):
        self.N = N
        self.M = M
        self.X = X
        self.limit = limit
        self.unit_cost = unit_cost
