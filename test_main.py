import unittest
from mongo_csv_editer import Db2Csv

import logging
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId

class TestDBtoCsv(unittest.TestCase):
    '''test db2csv module'''
    def setUp(self):
        product = MongoClient()['test'].product
        pass
        product.drop()
        data = [
                {'name': 'kami', 'age': 11},
                {'name': 'kamisama', 'age': 12} 
                ]
        product.insert(data)
        self.test_target = Db2Csv(product)

    def test_output(self):
        self.test_target.output_to_csv('unittest_data/test_output.csv', 'name', 'age')
        output_answer = open('unittest_data/test_output.csv','r').read()
        self.assertIsNotNone(output_answer)


#    def test_write_in(self):
#        pass

if __name__ == "__main__":
    unittest.main()
