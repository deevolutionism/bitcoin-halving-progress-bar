import unittest
from SubsidyCalc import SubsidyCalculator
from TweetComposer import ProgressBar, Tweet
import json

class test_bar_output(unittest.TestCase):
    def test(self):
        self.assertEqual(service.gen_progress_string(0.25))



def test_api():
    user = api.me()
    print(user.name)

# 200 - 300 n = 250 % of n = ?

#response = service.run(publish=False)
#print(response)

# timeline = service.api.user_timeline()
#CURRENT_BLOCK_HEIGHT = service.get_block_height("https://blockchain.info/q/getblockcount")
#calc = service.SubsidyCalculator(INIT_MINING_SUBSIDY=50, HALVING_INTERVAL=210000, CURRENT_BLOCK_HEIGHT=CURRENT_BLOCK_HEIGHT)
#progress_bar = service.ProgressBar(500000)
#print(progress_bar())


subsidy = SubsidyCalculator(INIT_MINING_SUBSIDY=50,CURRENT_BLOCK_HEIGHT=200000,HALVING_INTERVAL=210000)
block_subsidy = subsidy.block_subsidy()
subsidy_era = subsidy.subsidy_era()
block_height_of_next_halving = subsidy.block_height_of_next_halving()
blocks_remaining = subsidy.blocks_remaining()
percent_complete = subsidy.percent_complete()
progress_bar = ProgressBar(percent_complete=percent_complete)
progress_bar = progress_bar.gen_progress_string()
tweet = Tweet(SUBSIDY_ERA=subsidy_era, SUBSIDY_AMOUNT=block_subsidy, PROGRESS_BAR=progress_bar, BLOCKS_REMAINING=blocks_remaining)


print('block subsidy ' + str(block_subsidy))
print('subsidy era ' + str(subsidy_era))
print('block height of next halving ' + str(block_height_of_next_halving))
print('blocks remaining: ' + str(blocks_remaining))
print('percent to next halving: ' + str(percent_complete))
print(progress_bar)
print(tweet.compose())


