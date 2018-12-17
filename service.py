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

def get_block_height():
    r = requests.get(constants.GET_BLOCK_HEIGHT)
    return int(r.text)

CURRENT_BLOCK_HEIGHT = get_block_height()
LAST_EVENT = utils.get_block_height_from_last_event(CURRENT_BLOCK_HEIGHT, constants.N_BLOCKS_TO_HALVE)
REWARD_ERA = utils.calc_reward_era(CURRENT_BLOCK_HEIGHT, constants.N_BLOCKS_TO_HALVE)
NEXT_EVENT = LAST_EVENT + constants.N_BLOCKS_TO_HALVE
PROGRESS = utils.calc_progress(CURRENT_BLOCK_HEIGHT, NEXT_EVENT)



print('current block height: ', CURRENT_BLOCK_HEIGHT)
print('last event: ', LAST_EVENT)
print('reward era: ', REWARD_ERA)
print('next event: ', NEXT_EVENT)
print('progress: ', PROGRESS)
