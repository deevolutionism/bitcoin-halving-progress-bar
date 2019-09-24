# bitcoin-halving-progress-bar
A twitter bot that calculates the progression towards Bitcoin's next halving event. This bot can be deployed as a lambda function.

# overview of each file

### SubsidyCalc.py 

this module contains all of the logic for calculating Bitcoin's subsidy amount, progress towards next halving event, and reward era given a number of important initilization parameters such as the current block height, initial mining subsidy, halving interval, and number of coins that make up a single bitcoin.

The service calculates the progress that has been made until the next bitcoin halving event via a progress bar ranging from 0 - 100%

halving events occur every 210,000 blocks

get the block height every 10 minutes,
adjust the calculation
tweet everytime a percentage of progress has been achieved

### SSMManager.py

the manager module is amazon specific module used for storing the currently computed percentage and for retrieving the previously computed percentage complete from a key value store.
more information about amazon SSM can be found [here](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html).

### supply.md

This file contains a table that shows all of bitcoins subsidy halvings, the era, the subsidy amount per block, and the total maximum number of sats that should be available at the end of each halving event.

| subsidy era | subsidy (sats) | total supply (sats) |
|-------------|----------------|---------------------|
|1            | 5000000000     | 1050000000000000
|2            | 2500000000     | 1575000000000000
|3            | 1250000000     | 1837500000000000
|...          |...             |...
|32           | 2              | 2099999997480000
|33           | 1              | 2099999997690000
|34           | 0              | 2099999997690000



example output


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
python -m unittest test_SubsidyCalculator.py
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
zip -g function.zip service.py
```

update lamba function via aws-cli

```
aws lambda update-function-code --function-name updateBitcoinProgressTwitterBot --zip-file fileb://function.zip
```

or run the update script: 
```
./update.sh
```







