# coding: utf-8
"""
server框架
"""
from unittest import TestCase

# simple server start
from pythonframework.servers.basehttp import run


class TestSimpleServer(TestCase):
    def setUp(self):
        run('127.0.0.1', 8000)

    def test_request(self):
        pass
# simple server end
