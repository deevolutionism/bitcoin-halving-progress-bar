import math

def calc_progress(blockheight, next_event, n_blocks_to_halve):
    return ( (next_event - blockheight) / n_blocks_to_halve )

def get_block_height_from_last_event(current_block_height, n_blocks_to_halve):
    # determine the block height of the last halving event
    # get currernt blockheight
    # divide it by the constant to determine how many events have occured
    # events * constant = block height of last event
    n_events = current_block_height / n_blocks_to_halve
    last_event_block_height = math.floor(n_events) * n_blocks_to_halve
    return last_event_block_height

def calc_reward_era(current_block_height, n_block_to_halve):
    # calcualte the reward era we are currently in. + 1 to account for the 0th block reward
    return math.floor((current_block_height / n_block_to_halve) + 1)