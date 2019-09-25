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
INIT_MINING_REWARD = 50

class SSM():
    def __init__(self, ssm_path):
        self.ssm_path = ssm_path
    
    def check_ssm_value(self, value):
        ssm_response = client.get_parameter(
            Name=self.ssm_path,
            WithDecryption=False
        )
        return ssm_response['Parameter']['Value'].find(str(value))

    def update_ssm_value(self, value):
        ssm_response = client.put_parameter(
            Name=self.ssm_path,
            Description='',
            Value=str(value),
            Type='String',
            Overwrite=True
        )

class ProgressBar():
    """Create a progess bar"""
    def __init__(self, percent_complete):
        self.percent_complete = percent_complete

    def gen_progress_string(self, bar_length=15):
        """create a progress bar of n length"""
        p = math.floor(scale(self.percent_complete, 0, 100, 0, bar_length))

        bar = map(lambda x:'█', range(p))
        bar = ''.join(bar)

        bar_empty = ''.join( map( lambda x:'░', range(bar_length - p) ) )
        bar = ''.join( [bar, bar_empty] )
        progress_string = str(math.floor(self.percent_complete))
        bar = ''.join([ bar, " ", progress_string, "%" ])
        return bar


def scale(val, val_min, val_max, scale_min, scale_max):
    return scale_min + (scale_max - scale_min) * ( (val - val_min) / (val_max - val_min))

class SubsidyCalculator():
    """
    Calculate the subsidy reward, reward era, 
    percentage completed until next halving, and other stats
    given some required constants
    such as the inital minind subsidy amount,
    the halving interval ( number of block between halvings),
    current block height, and the number of coins that make up a bitcoin
    """
    def __init__(self, CURRENT_BLOCK_HEIGHT, INIT_MINING_SUBSIDY, HALVING_INTERVAL, COIN):
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
        return self.INIT_MINING_SUBSIDY >> subsidy_era - 1
    
    def compose(self):
        data = {
            'subsidy_era': self.subsidy_era(),
            'subsidy_amount': self.block_subsidy(),
            'blocks_remaining': self.blocks_remaining_until_next_halving(),
            'percent_complete': self.percent_complete()
        }
        return data


INIT_MINING_SUBSIDY = 50
COIN = 100000000
HALVING_INTERVAL = 210000
CURRENT_BLOCK_HEIGHT = 1
calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, CURRENT_BLOCK_HEIGHT=CURRENT_BLOCK_HEIGHT, COIN=COIN)
print(calc.block_subsidy())


class Tweeter():
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
            'Subsidy Era: ', str(self.SUBSIDY_ERA), '/33\n',
            'Block Subsidy: ', str(self.SUBSIDY_AMOUNT), 'BTC\n',
            'Blocks Remaining: ', str(self.BLOCKS_REMAINING), '\n',
            self.PROGRESS_BAR
        ])
        return status

def run(event="", context="", publish=True):
    # input event parameter of the backend Lambda function as follows:
    # {
    #     "resource": "Resource path",
    #     "path": "Path parameter",
    #     "httpMethod": "Incoming request's method name"
    #     "headers": {Incoming request headers}
    #     "queryStringParameters": {query string parameters }
    #     "pathParameters":  {path parameters}
    #     "stageVariables": {Applicable stage variables}
    #     "requestContext": {Request context, including authorizer-returned key-value pairs}
    #     "body": "A JSON string of the request payload."
    #     "isBase64Encoded": "A boolean flag to indicate if the applicable request payload is Base64-encode"
    # }


    response = {
        "statusCode": 200,
        "body": json.dumps(event['body'])
    }

    print(status)
    return response