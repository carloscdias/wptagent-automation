#!/bin/bash

randomGeneratorFile="/home/pi/wptagent-automation/scripts/generate_exponential.py"
timestampFile="/home/pi/wptagent-automation/timestamp_puppeteer"
logFile="/home/pi/wptagent-automation/log_puppeteer"

# timestamp in milliseconds
timestamp=$(($(date +%s%N)/1000000))

# interval in milliseconds
# sampling from exponential distribution with 30 minutes mean
interval="$(python3 $randomGeneratorFile 30)"

timestampNext=$(($timestamp + $interval))

echo "$(date +%s) | schedule PUPPETEER -> next timestamp $timestampNext" >> $logFile
echo $timestampNext > $timestampFile
