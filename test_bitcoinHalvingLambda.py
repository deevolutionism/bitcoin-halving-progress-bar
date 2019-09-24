import unittest
from bitcoinHalvingLambda import SubsidyCalculator
from bitcoinHalvingLambda import ProgressBar
from bitcoinHalvingLambda import Tweet
import math

class TestSubsidyCalc(unittest.TestCase):
    
    def test_subsidy_era_bitcoin(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 210000 * 33
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, CURRENT_BLOCK_HEIGHT=CURRENT_BLOCK_HEIGHT, COIN=100000000)
        result = calc.subsidy_era()
        print(result)
        self.assertEqual(result, 33)
    
    def test_blocks_remaining_until_next_halving(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 1
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, CURRENT_BLOCK_HEIGHT=1, COIN=100000000)
        self.assertEqual(calc.blocks_remaining_until_next_halving(), 209999)

    def test_block_height_of_next_halving(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 1
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, CURRENT_BLOCK_HEIGHT=1, COIN=100000000)
        self.assertEqual(calc.block_height_of_next_halving(), 210000)

    def test_percent_complete(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 210000
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, CURRENT_BLOCK_HEIGHT=210000, COIN=100000000)
        self.assertEqual(calc.percent_complete(), 100.0)

    def test_block_subsidy(self):
        INIT_MINING_SUBSIDY = 50
        i = 1
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 210000
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, CURRENT_BLOCK_HEIGHT=1, COIN=100000000)
        init_subsidy = INIT_MINING_SUBSIDY * COIN
        subsidy = init_subsidy
        supply = 0
        max_supply = 2099999997690000
        # print('block height', ':', 'subsidy era', ':', 'subsidy (sats)', ':', 'total supply (sats)')
        # for i in range(1,34):
        #     supply = supply + subsidy * HALVING_INTERVAL
        #     print('|', HALVING_INTERVAL * i, '|', i, '|', subsidy, '|', supply)
        #     subsidy = init_subsidy >> i
        #     i = i + 1
        result = calc.block_subsidy()
        print(result)
        self.assertEqual(result, 50*COIN)

class TestProgressBar(unittest.TestCase):
    def test_progress_bar_100(self):
        # input
        progressBar = ProgressBar(percent_complete=100)
        result = progressBar.gen_progress_string()
        self.assertEqual(result, '███████████████ 100%')
    
    def test_progress_bar_0(self):
        progressBar = ProgressBar(percent_complete=0)
        result = progressBar.gen_progress_string()

        self.assertEqual(result, '░░░░░░░░░░░░░░░ 0%')

class TestTweet(unittest.TestCase):
    def test_tweet_message(self):
        INIT_MINING_SUBSIDY = 50
        COIN = 100000000
        HALVING_INTERVAL = 210000
        CURRENT_BLOCK_HEIGHT = 210000 * 33
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, CURRENT_BLOCK_HEIGHT=CURRENT_BLOCK_HEIGHT, COIN=100000000)
        data = calc.compose()
        progressBar = ProgressBar(percent_complete=data['percent_complete'])
        progressBarString = progressBar.gen_progress_string()
        tweet = Tweet(SUBSIDY_ERA=data['subsidy_era'], SUBSIDY_AMOUNT=data['subsidy_amount'], BLOCKS_REMAINING=data['blocks_remaining'], PROGRESS_BAR=progressBarString)
        message = tweet.compose()
        self.assertEqual(message, "".join([
            'Subsidy Era: 33/33\n',
            'Block Subsidy: 1BTC\n',
            'Blocks Remaining: 0\n',
            '███████████████ 100%'
        ]))
