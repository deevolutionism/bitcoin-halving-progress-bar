import math
class SubsidyCalculator():
    """Calculate the subsidy reward, reward era, and other stats given some constants"""
    def __init__(self, INIT_MINING_SUBSIDY, HALVING_INTERVAL, CURRENT_BLOCK_HEIGHT, COIN):
        self.INIT_MINING_SUBSIDY = INIT_MINING_SUBSIDY * COIN
        self.HALVING_INTERVAL = HALVING_INTERVAL
        self.CURRENT_BLOCK_HEIGHT = CURRENT_BLOCK_HEIGHT

    def subsidy_era(self):
        return math.ceil((self.CURRENT_BLOCK_HEIGHT / self.HALVING_INTERVAL))

    def blocks_remaining(self):
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
        return self.INIT_MINING_SUBSIDY / (2**(subsidy_era - 1))

