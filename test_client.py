# -*- coding: utf-8 -*-

"""
This is a script with client tests.
"""
import client
import unittest
import unittest.mock

from threading import Thread


class TestClient(unittest.TestCase):
    def test_ip(self):
        with unittest.mock.patch('builtins.input', return_value='192.168.0.1'):
            self.assertEqual(client.get_server_ip(), '192.168.0.1')

    def test_port(self):
        with unittest.mock.patch('builtins.input', return_value='1111'):
            self.assertEqual(client.get_server_port(), 1111)

    def test_username(self):
        with unittest.mock.patch('builtins.input', return_value='user'):
            self.assertEqual(client.get_username(), 'user')

    def test_random_username(self):
        self.assertTrue(client.get_random_username())


if __name__ == '__main__':
    unittest.main()