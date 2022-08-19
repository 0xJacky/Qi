from auth3 import Auth
import unittest

class TestAuth3(unittest.TestCase):
    def test_auth3(self):
        auth = Auth()
        
        self.assertEqual(auth.login('201904020227', '132401@hero')[1], True)