"""Test for client.py that it implements its methods correctly"""
from client import GithubOrgClient
from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized

class TestGithubOrgClient(TestCase):
  """Testcase for testing GithubOrgClient class and its methods"""

  @parameterized.expand([("google"),("abc") ])
  @patch('client.get_json', return_value={"payload", True})
  def test_org(self, test_org,  mock):
    """Method to test that GithubOrgClient.org returns the correct value"""
    client = GithubOrgClient(test_org)
    res = client.org
    self.assertEqual(res, mock.return_value)
    mock.assert_called_once
