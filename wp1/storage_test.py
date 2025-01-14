import unittest
from unittest.mock import patch, MagicMock

from wp1.environment import Environment
from wp1.storage import connect_storage


class StorageTest(unittest.TestCase):

  def test_connect_storage_raises_if_no_env(self):
    with self.assertRaises(ValueError):
      actual = connect_storage()

  @patch('wp1.storage.ENV', Environment.DEVELOPMENT)
  def test_connect_storage_raises_if_no_credentials(self):
    with self.assertRaises(ValueError):
      actual = connect_storage()

  @patch('wp1.storage.CREDENTIALS', {Environment.DEVELOPMENT: {}})
  @patch('wp1.storage.ENV', Environment.DEVELOPMENT)
  def test_connect_storage_raises_if_no_storage_key(self):
    with self.assertRaises(ValueError):
      actual = connect_storage()

  @patch(
      'wp1.storage.CREDENTIALS', {
          Environment.DEVELOPMENT: {
              'STORAGE': {
                  'key': 'test_key',
                  'secret': 'test_secret',
                  'bucket': 'org-kiwix-dev-wp1',
              }
          }
      })
  @patch('wp1.storage.ENV', Environment.DEVELOPMENT)
  @patch('wp1.storage.KiwixStorage')
  def test_connect_storage_connects_to_kiwixstorage(self, patched_kiwixstorage):
    actual = connect_storage()
    patched_kiwixstorage.assert_called_once_with(
        'https://s3.us-west-1.wasabisys.com/'
        '?keyId=test_key&secretAccessKey=test_secret&bucketName=org-kiwix-dev-wp1'
    )

  @patch(
      'wp1.storage.CREDENTIALS', {
          Environment.DEVELOPMENT: {
              'STORAGE': {
                  'key': 'test_key',
                  'secret': 'test_secret',
                  'bucket': 'org-kiwix-dev-wp1',
              }
          }
      })
  @patch('wp1.storage.ENV', Environment.DEVELOPMENT)
  @patch('wp1.storage.KiwixStorage')
  def test_connect_storage_checks_permissions(self, patched_kiwixstorage):
    s3_mock = MagicMock()
    patched_kiwixstorage.return_value = s3_mock
    actual = connect_storage()
    s3_mock.check_credentials.assert_called_once_with(list_buckets=True,
                                                      bucket=True,
                                                      write=True,
                                                      read=True)
