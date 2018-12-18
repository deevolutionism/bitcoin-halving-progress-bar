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
import math
import constants
import utils
import requests
import tweepy
import auth

t_auth = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
t_auth.set_access_token(auth.access_token, auth.access_token_secret)
api = tweepy.API(t_auth)


def get_block_height():
    r = requests.get(constants.GET_BLOCK_HEIGHT)
    return int(r.text)

def gen_progress_string(progress):
    # ░
    # ▒
    # ▓
    # █
    # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ ████████▓░░░░░░░░░░░ 48% ┃
    # ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    # 20 * progress
    bar_length = 15
    c = bar_length * progress
    p = math.floor(c)
    f = (progress * 100) % (100 / bar_length)

    bar = map(lambda x:'█', range(p))
    bar = ''.join(bar)

    if 0 < f and f < 1:
        bar = bar + "░"
        pass
    elif 1 <= f and f < 2.5:
        bar = bar + "▒"
        pass
    elif 2.5 <= f and f < 4:
        bar = bar + "▓"
        pass

    bar = bar + ''.join( map( lambda x:'░', range(bar_length - p - 1) ) )

    bar = ''.join([ bar, " ", str(math.floor(progress * 100)), "%" ])
    return bar

def update_status(status):
    response = api.update_status(status)
    print(response)
    return response

def get_tweets():
    return

def run():
    # get the current block height from blockchain.info
    CURRENT_BLOCK_HEIGHT = get_block_height()
    # determine which blockheight the last halving event occured
    LAST_EVENT = utils.get_block_height_from_last_event(CURRENT_BLOCK_HEIGHT, constants.N_BLOCKS_TO_HALVE)
    # determine which reward era we are in
    REWARD_ERA = utils.calc_reward_era(CURRENT_BLOCK_HEIGHT, constants.N_BLOCKS_TO_HALVE)
    # determine the target blockheight for the next halving event
    NEXT_EVENT = LAST_EVENT + constants.N_BLOCKS_TO_HALVE
    # calculate current progress towards reaching the next halving event
    PROGRESS = utils.calc_progress(CURRENT_BLOCK_HEIGHT, NEXT_EVENT, constants.N_BLOCKS_TO_HALVE)
    # post to twitter only if progress has increased by a full percentage since the last tweet

    print('current block height: ', CURRENT_BLOCK_HEIGHT)
    print('last event: ', LAST_EVENT)
    print('reward era: ', REWARD_ERA)
    print('next event: ', NEXT_EVENT)
    print('progress: ', PROGRESS * 100)
    status = gen_progress_string(PROGRESS)
    print(status)
    update_status(status)


def test_api():
    user = api.me()
    print(user.name)


test_api()
run()