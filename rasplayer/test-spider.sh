#!/usr/bin/env bash

echo "Testing spider $1"
rm logs/$1.log
rm jsons/$1.json

scrapy crawl $1 -o jsons/$1.json -a mode=test --logfile logs/$1.log

echo "Done!"
echo "Check the log at logs/$1.log to make sure there are no errors, and the data at jsons/$1.json"
echo "Have a good day :)"