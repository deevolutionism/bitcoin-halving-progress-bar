import os
import requests
from . import SSM, ProgressBar, SubsidyCalculator, Tweeter, Tweet

def run(event="", context="", publish=True):
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
    calc = SubsidyCalculator(BLOCK_HEIGHT=CURRENT_BLOCK_HEIGHT, INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, COIN=100000000)
    
    # get the last computed value from storage
    ssm = SSM(ssm_path="/BitcoinProgress/lastKnownPercentage")
    prev_val = int(ssm.check_ssm_value())
    curr_val = curr_val = int(calc.percent_complete())

    BLOCK_HEIGHT = calc.BLOCK_HEIGHT
    SUBSIDY_ERA = calc.subsidy_era()
    SUBSIDY_AMOUNT = calc.block_subsidy()
    BLOCKS_REMAINING = calc.blocks_remaining_until_next_halving()
    PROGRESS_BAR = ProgressBar(percent_complete=curr_val).gen_progress_string()
    tweet = Tweet(BLOCK_HEIGHT=BLOCK_HEIGHT, SUBSIDY_ERA=SUBSIDY_ERA, SUBSIDY_AMOUNT=SUBSIDY_AMOUNT, BLOCKS_REMAINING=BLOCKS_REMAINING, PROGRESS_BAR=PROGRESS_BAR)


    if int(prev_val) < curr_val and publish == True:
        access_token = os.environ['twitter_access_token']
        access_token_secret = os.environ['twitter_access_token_secret']
        consumer_key = os.environ['twitter_consumer_key']
        consumer_secret = os.environ['twitter_consumer_secret']
        tweeter = Tweeter(access_token=access_token, access_token_secret=access_token_secret, consumer_key=consumer_key, consumer_secret=consumer_secret)
        message = tweet.compose()
        ssm.update_ssm_value(value=curr_val)
        response = 'test'
        response = tweeter.publishTweet(message)
        body= { "message": message, "prev val": prev_val, "curr val": curr_val, "published": publish, "twitter api response": response }
    else:
        body = { "message": "no update", "prev val": prev_val, "curr val": curr_val, "published": False }
    
    response = {
        "statusCode": 200,
        "body": body
    }

    print(body)
    return response
