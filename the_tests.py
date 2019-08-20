import unittest
from Checkout import Checkout

class TestCheckoutOrder(unittest.TestCase):
    def setUp(self):
        self.Checkout = Checkout()

    def test_createItemWeight(self):
        self.Checkout.createItemWeight("tuna fish", 3.56)
        tuna_fish_cost = self.Checkout.getItemCost("tuna fish")
        self.assertEqual(tuna_fish_cost, 3.56)

if __name__ == "__main__":
    unittest.main()
