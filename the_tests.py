import unittest
from Checkout import Checkout

class TestCheckoutOrder(unittest.TestCase):
    def setUp(self):
        self.Checkout = Checkout()

    def test_createItemWeight(self):
        self.Checkout.createItemWeight("tuna fish (weight)", 3.56)
        tuna_fish_cost = self.Checkout.getItemCost("tuna fish (weight)")
        self.assertEqual(tuna_fish_cost, 3.56)

    def test_removeItem(self):
        self.Checkout.createItemWeight("tuna fish (weight)", 3.56)
        self.Checkout.removeItem("tuna fish (weight)")
        with self.assertRaises(Exception):
            self.Checkout.getItemCost("tuna fish (weight)")

if __name__ == "__main__":
    unittest.main()
