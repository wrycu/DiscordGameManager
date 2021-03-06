from jsonschema import validate, ValidationError
from json import load
from src.config_schema import config_schema
import unittest

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_Config1(self):
        with open("config_test1.json") as data_file1:
            data1 = load(data_file1)
            with self.assertRaises(ValidationError):
                validate(data1, config_schema)

    def test_Config2(self):
        with open("config_test2.json") as data_file2:
            data2 = load(data_file2)
            with self.assertRaises(ValidationError):
                validate(data2, config_schema)

    def test_Config3(self):
        with open("config_test3.json") as data_file3:
            data3 = load(data_file3)
            self.assertEqual(None, validate(data3, config_schema))

    def test_Config4(self):
        with open("config_test4.json") as data_file4:
            data4 = load(data_file4)
            with self.assertRaises(ValidationError):
                validate(data4, config_schema)

    def test_Config5(self):
        with open("config_test5.json") as data_file5:
            data5 = load(data_file5)
            with self.assertRaises(ValidationError):
                validate(data5, config_schema)

if __name__ == '__main__':
    unittest.main()