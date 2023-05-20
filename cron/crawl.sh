#!/usr/bin/bash

cd $HOME/zapimoveis/zapimoveis/spiders
. $HOME/env/bin/activate
scrapy runspider zapspider.py
