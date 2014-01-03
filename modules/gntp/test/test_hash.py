# Copyright: 2013 Paul Traylor
# These sources are released under the terms of the MIT license: see LICENSE

"""
Test the various hashing methods

This test runs with the gntp.config module so that we can
get away without having to hardcode our password in a test
script. Please fill out your ~/.gntp config before running
"""
import os
from gntp.test import GNTPTestCase
from gntp.errors import UnsupportedError


class TestHash(GNTPTestCase):

	def _hash(self, hashName):
		self.growl.passwordHash = hashName
		return self._notify(description=hashName)

	def test_config(self):
		"""Test to see if our config file exists

		If our config file doesn't exist, then we have no
		password to test with, so our password hash is no good
		"""
		config = os.path.expanduser('~/.gntp')
		self.assertIsTrue(os.path.exists(config))

	def test_md5(self):
		self.assertIsTrue(self._hash('MD5'))

	def test_sha1(self):
		self.assertIsTrue(self._hash('SHA1'))

	def test_sha256(self):
		self.assertIsTrue(self._hash('SHA256'))

	def test_sha512(self):
		self.assertIsTrue(self._hash('SHA512'))

	def test_fake(self):
		'''Fake hash should not work'''
		self.growl.password = 'foobar'
		self.assertRaises(UnsupportedError, self._hash, 'fake-hash')
