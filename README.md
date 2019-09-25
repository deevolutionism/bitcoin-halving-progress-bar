# Bitcoin Halving Twitter Bot

A twitter bot that calculates the progression towards Bitcoin's next halving event.

![Subsidy Era: 3/33; Block Subsidy: ₿12.5; Blocks Remaining: 52389; Progress: 75%](https://gentrydemchak-portfolio-content.s3.amazonaws.com/bitcoin-progress.png)

## How the Bitcoin Halving works

The halving is a recurrent event that happens every 210,000 blocks that are mined. Each time a block is mined, the miner is rewarded with bitcoin via a special coinbase transaction. The coinbase transaction is a combination of The block subsidy and transaction fees. Transacton fees are accumulated over all transactions in the mined block and are added to the coinbase. The number of Fresh bitcoins to be minted is determined by the block subsidy and are added to the coinbase transaction. The initial block subsidy started at 50BTC and will continue to be cut in half every 210,000 blocks until the block subsidy reaches just 1 Satoshi at which point the subsidy can no longer be divided because it has reached the smallest denomination of a Bitcoin. This concludes the block subsidy halving lifecyle and end the supply of new Bitcoin. 

The block subsidy is a somewhat controversial, but important feature of the Bitcoin protocol because it determines the total supply of Bitcoin and the flow of new bitcoin.

---

## Overview

The bitcoinHalvingLambda.py module contains all of the logic for calculating Bitcoin's subsidy amount, progress towards next halving event, and reward era given a number of important initilization parameters such as the current block height, initial mining subsidy, halving interval, and number of coins that make up a single bitcoin. It also contains logic for posting to twitter, getting the current block height, and reading and writing to AWS SSM parameter storage.

I schedule the lambda run every 10 minutes, which is the aproximate time it takes for a new block to be found by miners.

* get the block height every 10 minutes
* recalculate progress
* Send a new tweet everytime a percentage of progress has been achieved

The AWS Lambda functions are best used stateless. However, this function depends on knowning the last computed percentage. We can't store that in the lambda function itself, so one way of getting that percentage is to store the value using the AWS Systems Manager Parameter Store.
more information about amazon SSM can be found [here](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html).

<<<<<<< HEAD
An alternative solution that would make this module less dependant on AWS might be to use a regex to find the percentage from the latest tweet.


### Total Bitcoin Supply
If you are curious to know the block subsidy amount for each subsidy era, I have generated a table in supply.md

| subsidy era | subsidy (sats) | total supply (sats) |
|-------------|----------------|---------------------|
|1            | 5000000000     | 1050000000000000
|2            | 2500000000     | 1575000000000000
|3            | 1250000000     | 1837500000000000
|...          |...             |...
|32           | 2              | 2099999997480000
|33           | 1              | 2099999997690000
|34           | 0              | 2099999997690000

=======
>>>>>>> 5b6f0b8ccac7e0e139574a4728f9125699b24d13

# setup
start the python virtual environment

### OSX
```
source ./bin/activate
```
set environemnt variables for twitter api access

### Windows
```
env\Scripts\activate.bat
```

# testing

### Testing subsidy calculator
using unittest you can run a test on the subsidy calculator

```
python -m unittest test_BitcoinHalvingLambda.py
```
### Testing twitter post
You will need a twitter account and api access.

# deploy to aws lambda
zip dependencies

```
cd package
zip -r9 ../function.zip .
cd ../
```

add function to zip

```
zip -g function.zip bitcoinHalvingLambda.py
```

update lamba function via aws-cli

```
aws lambda update-function-code --function-name updateBitcoinProgressTwitterBot --zip-file fileb://function.zip
```

or run the update script: 
```
./update.sh
```







