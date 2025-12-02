import unittest
from datetime import datetime
from lib.util import convert, get_json, sr_to_json, get_date_string
import pandas as pd

class TestUtil(unittest.TestCase):

    def test_convert(self):
        self.assertEqual(convert('100B'), 100)
        self.assertEqual(convert('1KB'), 1024)
        self.assertEqual(convert('1MB'), 1024 * 1024)
        self.assertEqual(convert('1GB'), 1024 * 1024 * 1024)
        self.assertEqual(convert('1TB'), 1024 * 1024 * 1024 * 1024)
        # Test case where unit is missing but B is assumed if regex matches?
        # Actually the regex in code expects unit.
        # Let's check logic: value = re.search(r'([0-9]+)', string); unit = re.search(r'([A-Z]?B)', string)

    def test_get_json(self):
        data = {'key': 'value', 'nested': {'inner': 123}}
        self.assertEqual(get_json('key', data), 'value')
        self.assertEqual(get_json('missing', data), 0)
        self.assertEqual(get_json('nested', data), {'inner': 123})

    def test_sr_to_json(self):
        series = ['a', 'b', 'a', 'c', 'b', 'b']
        # counts: b:3, a:2, c:1
        expected = {'b': 3, 'a': 2, 'c': 1}
        # Note: keys in json might be strings
        result = sr_to_json(series)
        self.assertEqual(result['b'], 3)
        self.assertEqual(result['a'], 2)
        self.assertEqual(result['c'], 1)

    def test_get_date_string(self):
        dt = datetime(2023, 10, 26, 12, 0, 0)
        result = get_date_string(dt)
        self.assertIn('2023-10-26', result)
