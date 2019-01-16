import unittest
import service
import tweepy
import json

class test_bar_output(unittest.TestCase):
    def test(self):
        self.assertEqual(service.gen_progress_string(0.25))


def test_api():
    user = api.me()
    print(user.name)

# 200 - 300 n = 250 % of n = ?

response = service.run(publish=False)
print(response)

# timeline = service.api.user_timeline()
