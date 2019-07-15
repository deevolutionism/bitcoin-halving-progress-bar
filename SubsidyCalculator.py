import math
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


INIT_MINING_SUBSIDY = 50
COIN = 100000000
HALVING_INTERVAL = 210000
CURRENT_BLOCK_HEIGHT = 1
calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, CURRENT_BLOCK_HEIGHT=CURRENT_BLOCK_HEIGHT, COIN=COIN)
print(calc.block_subsidy())