# -*- coding: utf-8 -*-

"""
This is a script with server tests.
"""
import server
import unittest


class TestServer(unittest.TestCase):
    def test_server_init(self):
        self.assertEqual(server.main(mode='test'), True)


if __name__ == '__main__':
    unittest.main()