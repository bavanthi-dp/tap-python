# task-8

import unittest
import os

class TestFiles(unittest.TestCase):

    def test1(self):
        self.assertTrue(os.path.exists("data/customers.csv"))

    def test2(self):
        self.assertTrue(os.path.exists("data/orders.csv"))

    def test3(self):
        self.assertTrue(os.path.exists("data/products.csv"))

    def test4(self):
        self.assertTrue(os.path.exists("data/sellers.csv"))

    def test5(self):
        self.assertTrue(os.path.exists("data/order_items.csv"))

if __name__ == "__main__":
    unittest.main()