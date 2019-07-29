# coding: utf-8
"""
工具框架
"""
from unittest import TestCase

# convert_util start
from pfbox.utils.convert_util import json_unpack, dict_unpack, list_unpack


class TestConvert(TestCase):
    def test_json_unpack(self):
        self.assertEqual(json_unpack('test'), 'test')
        self.assertEqual(json_unpack([1, 2, 3]), [1, 2, 3])
        self.assertEqual(json_unpack({'a': 1, 'b': 1}), {'a': 1, 'b': 1})
        self.assertEqual(json_unpack([{'a': 1, 'b': 1}, {'a': 2, 'b': 2}]), {'a': [1, 2], 'b': [1, 2]})
        self.assertEqual(json_unpack({'data': [{'a': 1, 'b': 1}, {'a': 2, 'b': 2}]}), {'a': [1, 2], 'b': [1, 2]})
        self.assertEqual(json_unpack({'data': [{'a': 1, 'b': 1}, {'a': 2, 'b': 2}], 'data1': 'test'}),
                         {'a': [1, 2], 'b': [1, 2], 'data1': 'test'})

    def test_dict_unpack(self):
        self.assertEqual(dict_unpack({'a': [{'c': 1}, {'c': 2}, {'c': 3}], 'b': 1}), {'c': [1, 2, 3], 'b': 1})
        self.assertEqual(dict_unpack({'a': {'d': 1, 'c': 1}, 'b': 1}), {'d': 1, 'c': 1, 'b': 1})

    def test_list_unpack(self):
        self.assertEqual(list_unpack([1, 2, 3]), [1, 2, 3])
        self.assertEqual(list_unpack([{'a': [1, 2], 'b': 1}, {'a': 2, 'b': 2}]), {'a': [1, 2, 2], 'b': [1, 2]})
        self.assertEqual(list_unpack([{'a': 1, 'b': 1}, {'a': 2, 'b': 2}]), {'a': [1, 2], 'b': [1, 2]})
        self.assertEqual(list_unpack([{'a': [{'c': {'d': [1, 1], 'e': 1}}, {'c': {'d': [2, 2], 'e': 2}}], 'b': 5},
                                      {'a': [{'c': {'d': [3, 2], 'e': 3}}, {'c': {'d': [4, 4], 'e': 4}}], 'b': 6}]),
                         {'b': [5, 6], 'd': [1, 1, 2, 2, 3, 2, 4, 4], 'e': [1, 2, 3, 4]})


# converts end

# zip_util start
from pfbox.utils.zip_util import create_zip_file


class TestZip(TestCase):
    def test_create_zip(self):
        create_zip_file('../pfbox', 'test.zip')
