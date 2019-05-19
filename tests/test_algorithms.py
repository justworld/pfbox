# coding: utf-8
"""
算法
"""
from unittest import TestCase

# sorts start
from pythonframework.algorithms.sorts import *


class TestSort(TestCase):
    def test_quick_sort(self):
        """
        测试快送排序
        """
        plain_list1 = [21, 16, 7, 1, 13, 29, 11, 12, 24]
        plain_list2 = [21, 16, 7, 1, 13, 29, 11, 12, 24, 22]
        quick_sort(plain_list1)
        self.assertEqual(plain_list1, [1, 7, 11, 12, 13, 16, 21, 24, 29])
        quick_sort(plain_list2)
        self.assertEqual(plain_list2, [1, 7, 11, 12, 13, 16, 21, 22, 24, 29])
