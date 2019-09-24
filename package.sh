#!/bin/bash
# zip -g functions.zip -r package service.py
# aws lambda update-function-code --function-name updateBitcoinProgressTwitterBot --zip-file fileb://function.zip
# aws lambda update-function
7z a -tzip function.zip package service.py
