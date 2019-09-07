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
        self.Checkout.create_item_db_count("watermelon", 5)
        self.Checkout.create_item_db_count("doritos", 2)
        self.Checkout.create_item_db_count("lemon", 2)


    def test_createItemDbWeight(self):
        self.createItemDatabase()
        tuna_fish_cost = self.Checkout.get_item_cost("tuna fish (weight)")
        self.assertEqual(tuna_fish_cost, 5.24)

    def test_removeItemDb(self):
        self.createItemDatabase()
        self.Checkout.remove_item_db("tuna fish (weight)")
        with self.assertRaises(Exception):
            self.Checkout.get_item_cost("tuna fish (weight)")

    def test_add_duplicate_item(self):
        self.Checkout.create_item_db_count("tuna fish (can)", 3.00)
        with self.assertRaises(Exception):
            self.Checkout.create_item_db_count("tuna fish (can)", 2.00)

    def test_scan_one_weight_item_get_total(self):
        self.createItemDatabase()
        # Since each item is unique wrt the units of measurement, no need to specify units
        self.Checkout.scan("tuna fish (weight)", 3)
        cart_cost = self.Checkout.get_cart_total()
        self.assertEqual(cart_cost, 5.24*3)

    def test_scan_one_count_item_get_total(self):
        self.createItemDatabase()
        self.Checkout.scan("donuts (dozen)")
        cart_cost = self.Checkout.get_cart_total()
        self.assertEqual(cart_cost, 3)

    def test_unscan_one_count_item(self):
        self.createItemDatabase()

        self.Checkout.scan("donuts (dozen)")
        in_cart = self.Checkout.is_item_in_cart("donuts (dozen)")
        self.assertEqual(in_cart[0], True)

        self.Checkout.unscan("donuts (dozen)")
        in_cart = self.Checkout.is_item_in_cart("donuts (dozen)")
        self.assertEqual(in_cart[0], False)

    def test_add_markdown(self):
        self.Checkout.add_markdown("watermelon", 0.5)
        markdown = self.Checkout.get_markdown("watermelon")
        self.assertEqual(markdown, 0.5)

        with self.assertRaises(Exception):
            self.Checkout.get_markdown("lemon")

    def test_one_count_item_with_markdown_total(self):
        self.createItemDatabase()
        self.Checkout.add_markdown("watermelon", 0.1)

        self.Checkout.scan("watermelon")
        cart_total = self.Checkout.get_cart_total()
        self.assertEqual(cart_total, 4.9)

    def test_one_weight_item_with_markdown_total(self):
        self.createItemDatabase()
        self.Checkout.add_markdown("tuna fish (weight)", 0.5)

        self.Checkout.scan("tuna fish (weight)", 4)
        cart_total = self.Checkout.get_cart_total()
        self.assertEqual(cart_total, 4*(5.24-0.5))

    def test_items_with_markdown(self):
        self.createItemDatabase()
        self.Checkout.add_markdown("doritos", .1)

        self.Checkout.scan("doritos")
        self.Checkout.scan("doritos")
        self.Checkout.scan("tuna fish (weight)", 2)
        cart_total = self.Checkout.get_cart_total()
        self.assertEqual(cart_total, 2*(2-.1) + 2*5.24)

    def test_count_special_N_for_X(self):
        self.createItemDatabase()
        self.Checkout.add_count_special_N_for_X("doritos", 3, 5)

        # 1
        self.Checkout.scan("doritos")
        total = self.Checkout.get_cart_total()
        self.assertEqual(total, 2)

        # 2
        self.Checkout.scan("doritos")
        total = self.Checkout.get_cart_total()
        self.assertEqual(total, 4)

        # 3
        self.Checkout.scan("doritos")
        total = self.Checkout.get_cart_total()
        self.assertEqual(total, 5)

        # 4
        self.Checkout.scan("doritos")
        total = self.Checkout.get_cart_total()
        self.assertEqual(total, 7)

        # 5
        self.Checkout.scan("doritos")
        total = self.Checkout.get_cart_total()
        self.assertEqual(total, 9)

        # 6
        self.Checkout.scan("doritos")
        total = self.Checkout.get_cart_total()
        self.assertEqual(total, 10)

    def test_count_special_N_for_X_limits(self):
        self.createItemDatabase()
        self.Checkout.add_count_special_N_for_X("doritos", 3, 5, 3)

        #
        self.Checkout.scan("doritos")
        self.Checkout.scan("doritos")
        self.Checkout.scan("doritos")

        total = self.Checkout.get_cart_total()
        self.assertEqual(total, 5)

        self.Checkout.scan("doritos")
        self.Checkout.scan("doritos")
        self.Checkout.scan("doritos")

        total = self.Checkout.get_cart_total()
        self.assertEqual(total, 11)


if __name__ == "__main__":
    unittest.main()
