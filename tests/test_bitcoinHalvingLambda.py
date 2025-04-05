import unittest
from src.bitcoinHalvingLambda import SubsidyCalculator
from src.bitcoinHalvingLambda import ProgressBar
from src.bitcoinHalvingLambda import Tweet

COIN = 100_000_000
HALVING_INTERVAL = 210000
INIT_MINING_SUBSIDY = 50

class TestSubsidyCalc(unittest.TestCase):
    
    def test_halving_interval_bitcoin(self):
        n_halvings = 64
        BLOCK_HEIGHT = 210000 * n_halvings
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=BLOCK_HEIGHT, COIN=COIN)
        result = calc.halvings()
        print(result)
        self.assertEqual(result, n_halvings)
      
    def test_4_halvings(self):
        BLOCK_HEIGHT = HALVING_INTERVAL * 4
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=BLOCK_HEIGHT, COIN=COIN)
        result = calc.halvings()
        print(result)
        self.assertEqual(result, 4)

    def test_blocks_remaining_until_next_halving(self):
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=1, COIN=COIN)
        self.assertEqual(calc.blocks_remaining_until_next_halving(), 209999)

    def test_block_height_of_next_halving(self):
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=1, COIN=COIN)
        self.assertEqual(calc.block_height_of_next_halving(), 210000)

    def test_percent_complete(self):
        expected_percent = []
        percent = []
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=210000, COIN=COIN)
        
        for x in range(1,101):
            if x == 1: 
                expected_percent.append(100.0)
            else:
                expected_percent.append(float(x-1))
            percent.append(calc.percent_complete()) 
            calc.BLOCK_HEIGHT += 2100 # halving_interval / 100

        print(expected_percent)
        self.assertListEqual(percent, expected_percent)

    def test_block_subsidy(self):
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=1, COIN=COIN)
        result = calc.block_subsidy()
        # print(result)
        self.assertEqual(result, 50*COIN)
    
    def test_block_subsidy_450000(self):
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=210001, COIN=COIN)
        result = calc.block_subsidy()
        # print(result)
        self.assertEqual(result, 25*COIN)
    
    def test_block_subsidy_all(self):
        HALVING_INTERVAL = 210000
        INIT_SUBSIDY = 50 * COIN
        MAX_HALVINGS = 64
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=0, COIN=COIN)
        subsidy = []
        expected_subsidy = []
        for x in range(0,MAX_HALVINGS):
            expected_subsidy.append(
                INIT_SUBSIDY >> x
            )

        # print("expected subsidy: ", expected_subsidy)

        for x in range(0,MAX_HALVINGS):
            sub = calc.block_subsidy()
            # print(calc.BLOCK_HEIGHT, sub, calc.subsidy_era())
            subsidy.append(sub)
            calc.BLOCK_HEIGHT += HALVING_INTERVAL
        self.assertListEqual(subsidy, expected_subsidy)

    def test_total_supply(self):
        HALVING_INTERVAL = 210000
        MAX_HALVINGS = 64
        COIN = 100000000
        INIT_SUBSIDY = INIT_MINING_SUBSIDY * COIN
        total_supply = INIT_SUBSIDY * HALVING_INTERVAL
        for x in range(1, MAX_HALVINGS):
            subsidy = INIT_SUBSIDY >> x
            total_supply += (HALVING_INTERVAL * subsidy)
            print(subsidy)
        expected_supply = 2099999997690000
        self.assertEqual(total_supply, expected_supply)
            

class TestProgressBar(unittest.TestCase):
    def test_progress_bar_100(self):
        # input
        progressBar = ProgressBar(percent_complete=100)
        result = progressBar.gen_progress_string()
        self.assertEqual(result, '███████████████ 100%')

    def test_progress_bar_99(self):
        progressBar = ProgressBar(percent_complete=99)
        result = progressBar.gen_progress_string()

        self.assertEqual(result, '██████████████░ 99%')
    
    def test_progress_bar_0(self):
        progressBar = ProgressBar(percent_complete=0)
        result = progressBar.gen_progress_string()

        self.assertEqual(result, '░░░░░░░░░░░░░░░ 0%')

class TestTweet(unittest.TestCase):
    def test_tweet_message(self):
        BLOCK_HEIGHT = 210000
        calc = SubsidyCalculator(INIT_MINING_SUBSIDY=INIT_MINING_SUBSIDY, HALVING_INTERVAL=HALVING_INTERVAL, BLOCK_HEIGHT=BLOCK_HEIGHT, COIN=COIN)
        data = calc.compose()
        progressBar = ProgressBar(percent_complete=data['percent_complete'])
        progressBarString = progressBar.gen_progress_string()
        tweet = Tweet(BLOCK_HEIGHT=data['block_height'], HALVINGS=data['halvings'], SUBSIDY_AMOUNT=data['subsidy_amount'], BLOCKS_REMAINING=data['blocks_remaining'], PROGRESS_BAR=progressBarString)
        message = tweet.compose()
        self.assertEqual(message, "".join([
            'Block Height: ', str(BLOCK_HEIGHT), '\n',
            'Halvenings: 1/64\n',
            'Block Subsidy: ₿25.0\n',
            'Blocks Remaining: 0\n',
            '███████████████ 100%'
        ]))


if __name__ == '__main__':
    unittest.main()