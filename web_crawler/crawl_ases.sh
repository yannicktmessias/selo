#!/bin/bash

# dentro da pasta do crawler
cd /home/ubuntu/workspace/selo/web_crawler

# usando o virutal env
source /home/ubuntu/workspace/selo/env/bin/activate

# executa o crawler
python -m scrapy crawl ases --logfile log.txt --set LOG_LEVEL=WARNING