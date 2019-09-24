# https://en.bitcoin.it/wiki/Controlled_supply
# get block height
# https://blockchain.info/q/getblockcount

# calculate progress:
# halving_constant = 210,000
# last_event = 210,000
# next_event = last_height + halving_constant
# blockheight = https://blockchain.info/q/getblockcount
# progress = ( blockheight / next_event ) * 100
# if progress > 100, update last_event, update next_event
# this twitter bot can finally rest once we have reached the 34th reward era.
# publish a tweet everytime progress has increased by a full percentage
# at 100%, publish something exciting!
import os
import json
import math
import requests
# import tweepy
# import boto3

# from SubsidyCalc import SubsidyCalculator
# from TweetComposer import Tweet
# from TweetComposer import TwitterHandler
# from SSMManager import SSM
# from ProgressBar import ProgressBar


# check ssm tag value
# calculate progress
# if ssm tag value is different:
# update ssm value
# publish tweet

# def start(event, context):

#     subsidy = SubsidyCalculator(
#         event['INIT_MINING_SUBSIDY'], 
#         event['HALVING_INTERVAL'],
#         event['CURRENT_BLOCK_HEIGHT']
#     )
#     ssm = SSM(event['SSM_PATH'])
#     ssm_val = ssm.check_ssm_value()

# # AWS SSM
# client = boto3.client('ssm')

# keys
# access_token = os.environ['twitter_access_token']
# access_token_secret = os.environ['twitter_access_token_secret']
# consumer_key = os.environ['twitter_consumer_key']
# consumer_secret = os.environ['twitter_consumer_secret']
# BTC defined constant: n blocks bewteen halving events
# HALVING_INTERVAL = 210000
# initial btc mining subsidy


# t_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# t_auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(t_auth)






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