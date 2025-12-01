# test_binary_search_tree.py

import unittest
from binary_search_tree import BinarySearchTree

class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.tree = BinarySearchTree()

    def test_insert(self):
        self.tree.insert(10)
        self.tree.insert(5)
        self.tree.insert(15)
        self.assertEqual(self.tree.search(10).value, 10)
        self.assertEqual(self.tree.search(5).value, 5)
        self.assertEqual(self.tree.search(15).value, 15)

    def test_delete(self):
        self.tree.insert(10)
        self.tree.insert(5)
        self.tree.delete(5)
        self.assertIsNone(self.tree.search(5))

    def test_is_valid_bst(self):
        self.tree.insert(10)
        self.tree.insert(5)
        self.tree.insert(15)
        self.assertTrue(self.tree.is_valid_bst())

if __name__ == "__main__":
    unittest.main()
