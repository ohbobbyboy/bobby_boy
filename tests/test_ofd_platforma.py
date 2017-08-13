#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import ofd
import config


class TestOFDTaxcom(unittest.TestCase):

    """ E2E unittest OFD-interactions """
    OFD = None

    @classmethod
    def setUpClass(cls):
        """ Setup """
        config.debug = False
        cls.OFD = ofd.OFDProvider(True).detect(
            "t=20170714T1311&s=35.00&fn=8710000100837497&i=231&fp=2921685295&n=1")

    def test_search(self):
        self.assertIsNotNone(self.OFD)

    def test_items_parsing(self):
        self.assertNotEqual(self.OFD.get_items(), [])

    def test_items_count(self):
        self.assertEqual(len(self.OFD.get_items()), 1)

    def test_first_item(self):
        item_name = self.OFD.get_items()[0][0]
        self.assertEqual(item_name, "Пицца Маргарита 1 шт.")

    def test_receipt_total_sum(self):
        self.assertEqual(self.OFD.total_sum, '35.00')

    def test_receipt_final_sum(self):
        self.assertEqual(self.OFD.raw_sum, '35.00')

if __name__ == '__main__':
    unittest.main()
