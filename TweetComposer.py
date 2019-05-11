import math
from scale import scale
import os
import json
import math
import requests
import tweepy

class TwitterHandler():
    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret, ssm_tag):
        self.access_token = os.environ[access_token]
        self.access_token_secret = os.environ[access_token_secret]
        self.consumer_key = os.environ[consumer_key]
        self.consumer_secret = os.environ[consumer_secret]

    def publishTweet(content, ssm_tag_val):

        response = api.update_status(content)

        print(response)
        return response

class Tweet():
    def __init__(self, SUBSIDY_ERA, SUBSIDY_AMOUNT, BLOCKS_REMAINING, PROGRESS_BAR):
        self.SUBSIDY_ERA = SUBSIDY_ERA
        self.SUBSIDY_AMOUNT = SUBSIDY_AMOUNT
        self.BLOCKS_REMAINING = BLOCKS_REMAINING
        self.PROGRESS_BAR = PROGRESS_BAR

    def compose(self):
        status = "".join([
            'Subsidy Era: ', str(self.SUBSIDY_ERA), '/34\n',
            'Block Subsidy: ₿', str(self.SUBSIDY_AMOUNT), '\n',
            'Blocks Remaining: ', str(self.BLOCKS_REMAINING), '\n',
            self.PROGRESS_BAR
        ])
        return status
