import unittest
from Checkout import Checkout


class TestCheckoutOrder(unittest.TestCase):
    def setUp(self):
        self.Checkout = Checkout()

    def createItemDatabase(self):
        self.Checkout.create_item_db_weight("tuna fish (weight)", 5.24)
        self.Checkout.create_item_db_weight("carrots", 2)
        self.Checkout.create_item_db_weight("tomatoes", 4.2)
        self.Checkout.create_item_db_weight("potatoes", 3)

        self.Checkout.create_item_db_count("tuna fish (can)", 3.00)
        self.Checkout.create_item_db_count("pepsi (2 liter)", 2.5)
        self.Checkout.create_item_db_count("water (2 liter)", 1.0)
        self.Checkout.create_item_db_count("donuts (dozen)", 3)

    def test_createItemDbWeight(self):
        self.createItemDatabase()
        tuna_fish_cost = self.Checkout.get_item_cost("tuna fish (weight)")
        self.assertEqual(tuna_fish_cost, 5.24)

    def test_removeItemDb(self):
        self.createItemDatabase()
        self.Checkout.remove_item_db("tuna fish (weight)")
        with self.assertRaises(Exception):
            self.Checkout.get_item_cost("tuna fish (weight)")

    def test_add_one_item_to_cart(self):
        self.createItemDatabase()
        # Since each item is unique wrt the units of measurement, no need to specify units
        self.Checkout.encart("tuna fish (weight)", 3)
        cart_cost = self.Checkout.get_cart_total()

        self.assertEqual(cart_cost, 5.24*3)

    #def test_scanItem(self):


if __name__ == "__main__":
    unittest.main()
