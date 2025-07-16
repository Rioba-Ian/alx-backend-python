#!/usr/bin/env python3

from  unittest import TestCase
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(TestCase):
  """Class that defines attributes to test utils.access_nested_map func"""
  @parameterized.expand([
    ({"a": 1},("a",), 1),
    ({"a": {"b": 2}},  ("a",), {"b": 2}),
    ( {"a": {"b": 2}}, ("a", "b"), 2)
  ])
  def test_access_nested_map(self, nested_map, path, expected):
    """Method to test that access nested map returns the right result"""
    self.assertEqual(access_nested_map(nested_map, path), expected)

  @parameterized.expand([
    ({}, ("a",)),
    ({"a": 1}, ("a","b"))
  ])
  def test_access_nested_map_exception(self, nested_map, path):
    """Method to test that exception is raised for access nested map"""
    with self.assertRaises(KeyError) as err:
      access_nested_map(nested_map, path)
    self.assertEqual(err.exception.args[0], path[-1])
