# bitcoin-halving-progress-bar
A twitter bot that calculates the progression towards Bitcoin's next halving event.


how the service works

calculate how much time is left until the next bitcoin halving event via a progress bar ranging from 0 - 100%

halving events occur every 210,000 blocks

get the block height every 10 minutes,
adjust the calculation
tweet everytime a percentage of progress has been achieved

example output
+------------------------+
|progress: 50%           |
|Era: 3                  |
|Supply: 18,000,000      |


Reward Era: 3
Reward: 6.5 BTC
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ████████▓▒░░░░░░░░░░ 48% ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

# setup
start the virtual environment
`source ./bin/activate`
set environemnt variables for twitter api access

# deploy to aws lambda
zip dependencies
`cd package`
`zip -r9 ../function.zip .`
`cd ../`

add function to zip
`zip -g function.zip service.py`

update lamba function
`aws lambda update-function-code --function-name updateBitcoinProgressTwitterBot --zip-file fileb://function.zip`


