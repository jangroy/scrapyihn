#!/usr/bin/env bash

echo "Running spider: $1 in real mode"

scrapy crawl $1 --logfile logs/$1.log