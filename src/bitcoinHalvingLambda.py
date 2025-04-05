import boto3
import math
import tweepy
from typing import Dict, Any

# BTC defined constant: n blocks bewteen halving events
HALVING_INTERVAL:int = 210000

# For now, depend on blockchain.info for getting latest block height
GET_BLOCK_HEIGHT = "https://blockchain.info/q/getblockcount"

# initial btc mining reward
INIT_MINING_SUBSIDY:int = 50

class SSM():
    def __init__(self, ssm_path: str) -> None:
        self.ssm_path = ssm_path
        self.client = boto3.client('ssm')
    
    def check_ssm_value(self) -> str:
        ssm_response = self.client.get_parameter(
            Name=self.ssm_path,
            WithDecryption=False
        )
        return ssm_response['Parameter']['Value']

    def update_ssm_value(self, value: str) -> None:
        self.client.put_parameter(
            Name=self.ssm_path,
            Description='',
            Value=str(value),
            Type='String',
            Overwrite=True
        )

class ProgressBar():
    """
    Create a progess bar that looks like this:

    █████████░░░░░
    """
    def __init__(self, percent_complete):
        self.percent_complete = percent_complete

    def gen_progress_string(self, bar_length=15):
        """create a progress bar of n length"""
        p = math.floor(scale(self.percent_complete, 0, 100, 0, bar_length))

        bar = map(lambda x:'█', range(p))
        bar = ''.join(bar)

        bar_incomplete = ''.join( map( lambda x:'░', range(bar_length - p) ) )
        bar = ''.join( [bar, bar_incomplete] )
        progress_string = str(math.floor(self.percent_complete))
        bar = ''.join([ bar, " ", progress_string, "%" ])
        return bar


def scale(val, val_min, val_max, scale_min, scale_max):
    return scale_min + (scale_max - scale_min) * ((val - val_min) / (val_max - val_min))

class SubsidyCalculator():
    """
    Calculate the subsidy reward, reward era, 
    percentage completed until next halving, and other stats
    given required constants and varaiables:
        BLOCK_HEIGHT: the most recent height of the bitcoin blockchain
        INIT_MINING_SUBSIDY: the initial mining subsidy. In bitcoins case, it is 50
        HALVING_INTERVAL: number of blocks between subsidy halvings. bitcoin default is every 210,000 block
        COIN: the total number of coins in a unit of bitcoin. Default is 100,000,000
    """
    def __init__(self, BLOCK_HEIGHT=0, INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, COIN=100000000):
        self.INIT_MINING_SUBSIDY = INIT_MINING_SUBSIDY * COIN
        self.HALVING_INTERVAL = HALVING_INTERVAL
        self.BLOCK_HEIGHT = BLOCK_HEIGHT
        self.COIN = COIN

    def halvings(self):
        return int(self.BLOCK_HEIGHT / self.HALVING_INTERVAL)

    def blocks_remaining_until_next_halving(self):
        if self.BLOCK_HEIGHT % self.HALVING_INTERVAL == 0:
            return 0  # No blocks remaining at the exact point of halving
        else:
            return self.block_height_of_next_halving() - self.BLOCK_HEIGHT

    def block_height_of_next_halving(self):
        n_halvings = self.halvings()
        next_event_block_height = (n_halvings * HALVING_INTERVAL) + HALVING_INTERVAL
        return next_event_block_height

    def percent_complete(self):
        max = self.block_height_of_next_halving()
        min = (self.halvings() * self.HALVING_INTERVAL)
        if self.BLOCK_HEIGHT - min == 0:
            return 100.0 
        return (self.BLOCK_HEIGHT - min) * 100 / (max - min)
    
    def halvings(self):
        # Adjust the halving calculation
        return min(int(self.BLOCK_HEIGHT / self.HALVING_INTERVAL), 64)

    def block_subsidy(self):
        n_halvings = self.halvings()
        # Adjust to account for a maximum of 64 halvings
        if n_halvings >= 64:
            return 0
        subsidy = self.INIT_MINING_SUBSIDY >> n_halvings
        return subsidy
    
    def compose(self):
        data = {
            'block_height': self.BLOCK_HEIGHT,
            'halvings': self.halvings(),
            'subsidy_amount': self.block_subsidy(),
            'blocks_remaining': self.blocks_remaining_until_next_halving(),
            'percent_complete': self.percent_complete()
        }
        return data


class Tweeter():
    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def publishTweet(self, content):
      try:
        t_auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        t_auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(t_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        response = api.update_status(content)
        print(f"Tweeted: {content}")
        return {"status": "success", "response": str(response)}
      except tweepy.TweepyException as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}

class Tweet():
    def __init__(self, BLOCK_HEIGHT, HALVINGS, SUBSIDY_AMOUNT, BLOCKS_REMAINING, PROGRESS_BAR):
        self.BLOCK_HEIGHT = BLOCK_HEIGHT
        self.HALVINGS = HALVINGS
        self.SUBSIDY_AMOUNT = SUBSIDY_AMOUNT
        self.BLOCKS_REMAINING = BLOCKS_REMAINING
        self.PROGRESS_BAR = PROGRESS_BAR

    def compose(self):
        status = "".join([
            'Block Height: ', str(self.BLOCK_HEIGHT), '\n',
            'Halvenings: ', str(self.HALVINGS), '/64\n',
            'Block Subsidy: ₿', str(self.SUBSIDY_AMOUNT / 100000000), '\n',
            'Blocks Remaining: ', str(self.BLOCKS_REMAINING), '\n',
            self.PROGRESS_BAR
        ])
        return status
