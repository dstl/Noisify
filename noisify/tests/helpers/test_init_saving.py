"""
.. Dstl (c) Crown Copyright 2019
"""
import unittest
from noisify.helpers import SavedInitStatement
from ast import literal_eval


class TestInitSaving(unittest.TestCase):
    def test_args(self):
        new_object = SavedInitStatement('a', 'b', 'c')
        self.assertEqual(literal_eval(new_object.init_statement), ('a', 'b', 'c'))
        pass

    def test_kwargs(self):
        new_object = SavedInitStatement(a='1', b='2', c='3')
        self.assertEqual(literal_eval(new_object.init_statement), {'a': '1', 'b': '2', 'c': '3'})
        pass

    def test_both(self):
        new_object = SavedInitStatement('a', 'b', c=1, d=2)
        args, kwargs = new_object.init_statement.split('-')
        self.assertEqual(literal_eval(args), ('a', 'b'))
        self.assertEqual(literal_eval(kwargs), {'c': 1, 'd': 2})
        pass
