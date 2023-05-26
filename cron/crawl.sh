#!/usr/bin/bash

cd /home/project_files/floripa-rent-watch/zapimoveis/zapimoveis/spiders
. /home/project_files/floripa-rent-watch/env/bin/activate
scrapy runspider zapspider.py
