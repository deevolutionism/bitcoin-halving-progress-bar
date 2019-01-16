#!/bin/bash
zip -g functions.zip service.py
aws lambda update-function-code --function-name updateBitcoinProgressTwitterBot --zip-file fileb://function.zip