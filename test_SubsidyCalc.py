import unittest
from SubsidyCalc import SubsidyCalculator
import math

class TestSubsidyCalc(unittest.TestCase):
    
    def test_subsidy_era_bitcoin(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 210000 * 34
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY, HALVING_INTERVAL, CURRENT_BLOCK_HEIGHT, COIN)
        result = calc.subsidy_era()
        print(result)
        self.assertEqual(result, 34)
    
    def test_blocks_remaining(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 1
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY, HALVING_INTERVAL, CURRENT_BLOCK_HEIGHT, COIN)
        self.assertEqual(calc.blocks_remaining(), 209999)

    def test_block_height_of_next_halving(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 1
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY, HALVING_INTERVAL, CURRENT_BLOCK_HEIGHT, COIN)
        self.assertEqual(calc.block_height_of_next_halving(), 210000)

    def test_percent_complete(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 210000
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY, HALVING_INTERVAL, CURRENT_BLOCK_HEIGHT, COIN)
        self.assertEqual(calc.percent_complete(), 100.0)

    def test_block_subsidy(self):
        INIT_MINING_SUBSIDY = 50
        i = 1
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 210000 * 1
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY, HALVING_INTERVAL, CURRENT_BLOCK_HEIGHT, COIN)
        subsidy = INIT_MINING_SUBSIDY * COIN
        supply = 0
        max_supply = 2099999997690000
        print('subsidy era', ':', 'subsidy (sats)', ':', 'total supply (sats)')
        while(i <= 34):
            supply = supply + subsidy * HALVING_INTERVAL
            print(i, ':', subsidy, ':', supply)
            subsidy = int( subsidy / 2 )
            i = i + 1
        result = calc.block_subsidy()
        print(result)
        self.assertEqual(result, 50*COIN)