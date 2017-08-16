#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import ofd
import config


class TestOFDYa(unittest.TestCase):

    """ E2E unittest OFD-interactions """
    OFD = None

    @classmethod
    def setUpClass(cls):
        """ Setup """
        config.debug = False
        cls.OFD = ofd.OFDProvider(True).detect(
            "t=20170305T005100&s=140.00&fn=8710000100161943&i=8018&fp=2398195357&n=1",
            "0000069245023747")

    def test_search(self):
        self.assertIsNotNone(self.OFD)

    def test_items_parsing(self):
        self.assertEqual(self.OFD.get_items(), [('Хлеб Ржаной  пол. рез. 0,415 кг (Каравай', '-28.40'), ('ФО Картофель, кг                       (17.9 * 1.132)', '-20.26'), ('ФО Огурцы Эстафета, кг                 (161.9 * 0.18)', '-29.14'), ('Яйцо фас. С0 10шт                     ', '-62.20')])

    def test_items_count(self):
        self.assertEqual(len(self.OFD.get_items()), 4)

    def test_first_item(self):
        item_name = self.OFD.get_items()[0][0]
        self.assertEqual(item_name, "Хлеб Ржаной  пол. рез. 0,415 кг (Каравай")

    def test_receipt_final_sum(self):
        self.assertEqual(self.OFD.raw_sum, '140.00')

if __name__ == '__main__':
    unittest.main()
