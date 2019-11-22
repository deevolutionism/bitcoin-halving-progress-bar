import boto3
import json
import os
import math
import requests
import tweepy

# AWS SSM
client = boto3.client('ssm')

# BTC defined constant: n blocks bewteen halving events
N_BLOCKS_TO_HALVE = 210000

# For now, depend on blockchain.info for getting latest block height
GET_BLOCK_HEIGHT = "https://blockchain.info/q/getblockcount"

# initial btc mining reward
INIT_MINING_SUBSIDY = 50

class SSM():
    def __init__(self, ssm_path):
        self.ssm_path = ssm_path
    
    def check_ssm_value(self):
        ssm_response = client.get_parameter(
            Name=self.ssm_path,
            WithDecryption=False
        )
        return ssm_response['Parameter']['Value']

    def update_ssm_value(self, value):
        ssm_response = client.put_parameter(
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
    return scale_min + (scale_max - scale_min) * ( (val - val_min) / (val_max - val_min))

class SubsidyCalculator():
    """
    Calculate the subsidy reward, reward era, 
    percentage completed until next halving, and other stats
    given required constants and varaiables:
        CURRENT_BLOCK_HEIGHT: the most recent height of the bitcoin blockchain
        INIT_MINING_SUBSIDY: the initial mining subsidy. In bitcoins case, it is 50
        HALVING_INTERVAL: number of blocks between subsidy halvings. bitcoin default is every 210,000 block
        COIN: the total number of coins in a unit of bitcoin. Default is 100,000,000
    """
    def __init__(self, CURRENT_BLOCK_HEIGHT=0, INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, COIN=100000000):
        self.INIT_MINING_SUBSIDY = INIT_MINING_SUBSIDY * COIN
        self.HALVING_INTERVAL = HALVING_INTERVAL
        self.CURRENT_BLOCK_HEIGHT = CURRENT_BLOCK_HEIGHT

    def subsidy_era(self):
        return math.ceil((self.CURRENT_BLOCK_HEIGHT / self.HALVING_INTERVAL))

    def blocks_remaining_until_next_halving(self):
        return self.block_height_of_next_halving() - self.CURRENT_BLOCK_HEIGHT

    def block_height_of_next_halving(self):
        era = self.subsidy_era() - 1
        next_event_block_height = era * self.HALVING_INTERVAL + self.HALVING_INTERVAL
        return next_event_block_height

    def percent_complete(self):
        max = self.block_height_of_next_halving()
        min = (self.subsidy_era() - 1) * self.HALVING_INTERVAL
        return (self.CURRENT_BLOCK_HEIGHT - min) * 100 / (max - min) 

    def block_subsidy(self):
        subsidy_era = self.subsidy_era()
        # use a bitwise right shift to halve the subsidy based on the era
        return self.INIT_MINING_SUBSIDY >> subsidy_era - 1
    
    def compose(self):
        data = {
            'subsidy_era': self.subsidy_era(),
            'subsidy_amount': self.block_subsidy(),
            'blocks_remaining': self.blocks_remaining_until_next_halving(),
            'percent_complete': self.percent_complete()
        }
        return data


class Tweeter():
    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret, ssm_tag):
        self.access_token = os.environ[access_token]
        self.access_token_secret = os.environ[access_token_secret]
        self.consumer_key = os.environ[consumer_key]
        self.consumer_secret = os.environ[consumer_secret]

    def publishTweet(self, content, ssm_tag_val):
        t_auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        t_auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(t_auth)
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
            'Subsidy Era: ', str(self.SUBSIDY_ERA), '/33\n',
            'Block Subsidy: ', str(self.SUBSIDY_AMOUNT), 'BTC\n',
            'Blocks Remaining: ', str(self.BLOCKS_REMAINING), '\n',
            self.PROGRESS_BAR
        ])
        return status

def run(event="", context="", publish=False):
    """
    input event parameter of the backend Lambda function as follows:
    {
        "resource": "Resource path",
        "path": "Path parameter",
        "httpMethod": "Incoming request's method name"
        "headers": {Incoming request headers}
        "queryStringParameters": {query string parameters }
        "pathParameters":  {path parameters}
        "stageVariables": {Applicable stage variables}
        "requestContext": {Request context, including authorizer-returned key-value pairs}
        "body": "A JSON string of the request payload."
        "isBase64Encoded": "A boolean flag to indicate if the applicable request payload is Base64-encode"
    }
    """
    CURRENT_BLOCK_HEIGHT = int(requests.get(GET_BLOCK_HEIGHT).text)
    calc = SubsidyCalculator(INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, CURRENT_BLOCK_HEIGHT=CURRENT_BLOCK_HEIGHT, COIN=100000000)
    
    # get the last computed value from storage
    ssm = SSM(ssm_path="/BitcoinProgress/lastKnownPercentage")
    prev_val = int(ssm.check_ssm_value())
    curr_val = curr_val = int(calc.percent_complete())

    SUBSIDY_ERA = calc.subsidy_era()
    SUBSIDY_AMOUNT = calc.block_subsidy()
    BLOCKS_REMAINING = calc.blocks_remaining_until_next_halving()
    PROGRESS_BAR = ProgressBar(percent_complete=curr_val).gen_progress_string()
    tweet = Tweet(SUBSIDY_ERA=SUBSIDY_ERA, SUBSIDY_AMOUNT=SUBSIDY_AMOUNT, BLOCKS_REMAINING=BLOCKS_REMAINING, PROGRESS_BAR=PROGRESS_BAR)


    if prev_val < curr_val and publish == True:
        access_token = os.environ['twitter_access_token']
        access_token_secret = os.environ['twitter_access_token_secret']
        consumer_key = os.environ['twitter_consumer_key']
        consumer_secret = os.environ['twitter_consumer_secret']
        tweeter = Tweeter(access_token=access_token, access_token_secret=access_token_secret, consumer_key=consumer_key, consumer_secret=consumer_secret)
        message = tweet.compose()
        tweeter.publishTweet(message)
        body= { "message": message, "prev val": prev_val, "curr val": curr_val, "published": publish}
    else:
        body = { "message": "", "prev val": prev_val, "curr val": curr_val, "published": publish }
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    print(body)
    return response