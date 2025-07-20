#!/usr/bin/env python3


"""Test for client.py that it implements its methods correctly"""
from requests.models import HTTPError
from client import GithubOrgClient
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD

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

  def test_public_repos_url(self):
    """Test that the result of _public_repos_url is the expected one based on mocked payload"""
    with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock, return_value={"repos_url": 'Test value'}) as mock:
      test_json = {"repos_url": "Test value"}
      client = GithubOrgClient(test_json.get("repos_url"))
      res = client._public_repos_url
      self.assertEqual(res, mock.return_value.get("repos_url"))
      mock.assert_called_once


  @patch('client.get_json', return_value={"name", "Test value"})
  def test_public_repos(self, mock):
    """Method to test that GithubOrgClient.org returns the correct value"""
    with patch.object(GithubOrgClient, '_public_repos_url',
             new_callable=PropertyMock,
             return_value="https://api.github.com/") as pub:
      client = GithubOrgClient("Test value")
      res = client.public_repos()

      self.assertEqual(res, ["Test value"])
      mock.assert_called_once
      pub.assert_called_once

  @parameterized.expand([
    ({"license": {"key": "my_license"}}, "my_license"),
    ({"license": {"key": "other_license"}}, "other_license"),
  ])
  def test_has_license(self, repo, license_key, expected):
    """Method to test that GithubOrgClient.has_license will return repo and whether has license"""
    client = GithubOrgClient("Test value")
    res = client.has_license(repo, license_key)
    self.assertEqual(res, expected)

@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(TestCase):
  """Integration test for GithubOrgClient, mocking code that sends external requests"""

  @classmethod
  def setUpClass(cls):
    """Method to prepare test fixture"""
    cls.get_patcher = patch('requests.get', side_effect=HTTPError)
    cls.get_patcher.start()

  @classmethod
  def tearDownClass(cls):
    """Method called after test method has been called"""
    cls.get_patcher.stop()


  def test_public_repos(self):
    res = GithubOrgClient("Test value")
    self.assertTrue(res)

  # @parameterized.expand()
  # def test_public_repos_with_license(self):
  #   res = GithubOrgClient("Test value").has_license()
