import unittest
from Checkout import Checkout


class TestCheckoutOrder(unittest.TestCase):
    def setUp(self):
        self.checkout = Checkout()

        # Create a local database that's separate from the Checkout database implementation
        # i.e. so that we're not simultaneously testing and using the Checkout database
        self.local_db = {
            "tuna fish (weight)": 5.24,
            "carrots": 3.5,
            "tomatoes": 4.2,
            "potatoes": 3,
            "tuna fish (can)": 3.4,
            "pepsi (2 liter)": 2.5,
            "water (2 liter)": 1.0,
            "donuts (dozen)": 4.1,
            "watermelon": 5,
            "doritos": 2.25,
            "lemon": 2,
        }
        
        self.createItemDatabase()

    def createItemDatabase(self):
        self.checkout.create_item_db_weight("tuna fish (weight)", self.local_db["tuna fish (weight)"])
        self.checkout.create_item_db_weight("carrots", self.local_db["carrots"])
        self.checkout.create_item_db_weight("tomatoes", self.local_db["tomatoes"])
        self.checkout.create_item_db_weight("potatoes", self.local_db["potatoes"])

        self.checkout.create_item_db_count("tuna fish (can)", self.local_db["tuna fish (can)"])
        self.checkout.create_item_db_count("pepsi (2 liter)", self.local_db["pepsi (2 liter)"])
        self.checkout.create_item_db_count("water (2 liter)", self.local_db["water (2 liter)"])
        self.checkout.create_item_db_count("donuts (dozen)", self.local_db["donuts (dozen)"])
        self.checkout.create_item_db_count("watermelon", self.local_db["watermelon"])
        self.checkout.create_item_db_count("doritos", self.local_db["doritos"])
        self.checkout.create_item_db_count("lemon", self.local_db["lemon"])

    def test_create_item_db_weight(self):
        # I have to reset the Checkout database in order for this test to be meaningful
        # due to the setUp() call
        self.checkout.reset_item_db()
        self.checkout.create_item_db_weight("tuna fish (weight)", self.local_db["tuna fish (weight)"])
        tuna_fish_cost = self.checkout.get_item_cost("tuna fish (weight)")
        self.assertAlmostEqual(tuna_fish_cost, self.local_db["tuna fish (weight)"])

    def test_removeItemDb(self):
        
        self.checkout.remove_item_db("tuna fish (weight)")
        cost = self.checkout.get_item_cost("tuna fish (weight)")
        self.assertAlmostEqual(cost, None)



    def test_scan_one_weight_item_get_total(self):
        
        # Since each item is unique wrt the units of measurement, no need to specify units
        self.checkout.scan("tuna fish (weight)", 3)
        cart_cost = self.checkout.get_cart_total()
        self.assertAlmostEqual(cart_cost, self.local_db["tuna fish (weight)"]*3)

    def test_scan_one_count_item_get_total(self):
        
        self.checkout.scan("donuts (dozen)")
        cart_cost = self.checkout.get_cart_total()
        self.assertAlmostEqual(cart_cost, self.local_db["donuts (dozen)"])

    def test_unscan_one_count_item(self):
        

        self.checkout.scan("donuts (dozen)")
        num_in_cart = self.checkout.get_num_in_cart("donuts (dozen)")
        self.assertGreater(num_in_cart, 0)

        self.checkout.unscan("donuts (dozen)")
        num_in_cart = self.checkout.get_num_in_cart("donuts (dozen)")
        self.assertEqual(num_in_cart, 0)

    def test_add_markdown(self):
        self.checkout.add_markdown("watermelon", 0.5)
        markdown = self.checkout.get_markdown("watermelon")
        self.assertAlmostEqual(markdown, 0.5)

        markdown = self.checkout.get_markdown("lemon")
        self.assertAlmostEqual(markdown, None)

    def test_one_count_item_with_markdown_total(self):
        
        markdown = 0.1
        self.checkout.add_markdown("watermelon", markdown)

        self.checkout.scan("watermelon")
        cart_total = self.checkout.get_cart_total()
        self.assertAlmostEqual(cart_total, self.local_db["watermelon"] - markdown)

    def test_one_weight_item_with_markdown_total(self):
        
        markdown = 0.5
        self.checkout.add_markdown("tuna fish (weight)", markdown)

        weight = 4
        self.checkout.scan("tuna fish (weight)", weight)
        cart_total = self.checkout.get_cart_total()
        self.assertAlmostEqual(cart_total, weight*(self.local_db["tuna fish (weight)"]-markdown))

    def test_items_with_markdown(self):
        
        
        doritos_markdown = 0.1
        self.checkout.add_markdown("doritos", doritos_markdown)

        self.checkout.scan("doritos")
        self.checkout.scan("doritos")
        doritos_cost = 2 * (self.local_db["doritos"] - doritos_markdown)

        weight_tuna = 2
        self.checkout.scan("tuna fish (weight)", weight_tuna)
        tuna_cost = weight_tuna * self.local_db["tuna fish (weight)"]

        cart_total = self.checkout.get_cart_total()

        self.assertAlmostEqual(cart_total, tuna_cost + doritos_cost)

    def test_count_special_N_for_X(self):
        
        self.checkout.add_count_special_N_for_X("doritos", 3, 5)

        # 1
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 1*self.local_db["doritos"])

        # 2
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 2*self.local_db["doritos"])

        # 3
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 5)

        # 4
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 5 + 1*self.local_db["doritos"])

        # 5
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 5 + 2*self.local_db["doritos"])

        # 6
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 10)

    def test_count_special_N_for_X_limits(self):
        
        self.checkout.add_count_special_N_for_X("doritos", 3, 5, 3)

        #
        self.checkout.scan("doritos")
        self.checkout.scan("doritos")
        self.checkout.scan("doritos")

        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 5)

        self.checkout.scan("doritos")
        self.checkout.scan("doritos")
        self.checkout.scan("doritos")

        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 5 + 3*self.local_db["doritos"])

    def test_count_special_N_M_X(self):
        
        self.checkout.add_special_N_M_X("doritos", 3, 2, 20)

        # 1
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, self.local_db["doritos"])

        # 2
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 2*self.local_db["doritos"])

        # 3
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3*self.local_db["doritos"])

        # 4
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3*self.local_db["doritos"] + 0.8*self.local_db["doritos"])

        # 5
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3*self.local_db["doritos"] + 0.8*2*self.local_db["doritos"])

        # 1
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.8*2*self.local_db["doritos"]) + (self.local_db["doritos"]))

        # 2
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.8*2*self.local_db["doritos"]) + (2*self.local_db["doritos"]))

        # 3
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.8*2*self.local_db["doritos"]) + (3*self.local_db["doritos"]))

        # 4
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.8*2*self.local_db["doritos"]) + (3*self.local_db["doritos"] + 0.8*self.local_db["doritos"]))

        # 5
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total,  (3*self.local_db["doritos"] + 0.8*2*self.local_db["doritos"]) + (3*self.local_db["doritos"] + 0.8*2*self.local_db["doritos"]))

    def test_count_special_N_M_X_limits(self):
        
        self.checkout.add_special_N_M_X("doritos", 3, 2, 60, 5)

        # 1
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 1*self.local_db["doritos"])

        # 2
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 2*self.local_db["doritos"])

        # 3
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3*self.local_db["doritos"])

        # 4
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3*self.local_db["doritos"] + 0.4*self.local_db["doritos"])

        # 5
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3*self.local_db["doritos"] + 0.4*2*self.local_db["doritos"])

        # 1
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.4*2*self.local_db["doritos"]) + 1*self.local_db["doritos"])

        # 2
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.4*2*self.local_db["doritos"]) + 2*self.local_db["doritos"])

        # 3
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.4*2*self.local_db["doritos"]) + 3*self.local_db["doritos"])

        # 4
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.4*2*self.local_db["doritos"]) + 4*self.local_db["doritos"])

        # 5
        self.checkout.scan("doritos")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3*self.local_db["doritos"] + 0.4*2*self.local_db["doritos"]) + 5*self.local_db["doritos"])

    def test_weight_special_N_M_X(self):
        

        self.checkout.add_special_N_M_X("carrots", 3, 1, 25)
        # 1 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3.5*1)

        # 2 - add 1 pound of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3.5*2)

        # 3 - add 1 pound of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3.5*3)

        # 4 - add 1 pound of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3.5*3 + 0.75*3.5*1)

        # 1 - add 1 pound of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5*3 + 0.75*3.5*1) + 3.5*1)

        # 2 - add 1 pound of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5 * 3 + 0.75 * 3.5 * 1) + 3.5 * 2)

        # 3 - add 1 pound of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5 * 3 + 0.75 * 3.5 * 1) + (3.5 * 3))

        # 4 - add 1 pound of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5 * 3 + 0.75 * 3.5 * 1) + (3.5 * 3 + 0.75*3.5*1))

    def test_weight_special_N_M_X_limit(self):
        

        self.checkout.add_special_N_M_X("carrots", 2, 1, 10, 6)
        # 1 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3.5*1)

        # 2 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 3.5*2)

        # 3 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5*2 + 0.9*3.5*1))

        # 1 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5*2 + 0.9*3.5*1) +(3.5*1))

        # 2 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5*2 + 0.9*3.5*1) +(3.5*2))

        # 3 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5 * 2 + 0.9 * 3.5 * 1) + (3.5 * 2 + 0.9*3.5*1))

        # 1 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5 * 2 + 0.9 * 3.5 * 1) + (3.5 * 2 + 0.9 * 3.5 * 1) + 3.5*1)

        # 2 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5 * 2 + 0.9 * 3.5 * 1) + (3.5 * 2 + 0.9 * 3.5 * 1) + 3.5 * 2)

        # 3 - add 1 pounds of carrots
        self.checkout.scan("carrots", 1)
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (3.5 * 2 + 0.9 * 3.5 * 1) + (3.5 * 2 + 0.9 * 3.5 * 1) + 3.5 * 3)

    def test_markdown_plus_special_with_limits(self):
        markdown = 0.5
        self.checkout.add_count_special_N_for_X("tuna fish (can)", 3, 5, 3)
        self.checkout.add_markdown("tuna fish (can)", markdown)

        # 1-1
        self.checkout.scan("tuna fish (can)")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (self.local_db["tuna fish (can)"]-markdown)*1)

        # 1-2
        self.checkout.scan("tuna fish (can)")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (self.local_db["tuna fish (can)"] - markdown) * 2)

        # 1-3
        self.checkout.scan("tuna fish (can)")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 5)

        self.checkout.unscan("tuna fish (can)")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (self.local_db["tuna fish (can)"] - markdown)*2)

        self.checkout.scan("tuna fish (can)")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, 5)

        # 2-1
        self.checkout.scan("tuna fish (can)")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (5) + (self.local_db["tuna fish (can)"] - markdown)*1)

        # 2-2
        self.checkout.scan("tuna fish (can)")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (5) + (self.local_db["tuna fish (can)"] - markdown) * 2)

        # 2-3
        self.checkout.scan("tuna fish (can)")
        total = self.checkout.get_cart_total()
        self.assertAlmostEqual(total, (5) + (self.local_db["tuna fish (can)"] - markdown)*3)


if __name__ == "__main__":
    unittest.main()
