import unittest
import service

class test_bar_output(unittest.TestCase):
    def test(self):
        self.assertEqual(service.gen_progress_string(0.25))


def test_api():
    user = api.me()
    print(user.name)