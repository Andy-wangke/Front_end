#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
#custom setting


subscribe_folder='subscribe/'

source_folder ='source/'

source_pretty_folder = 'source/pretty_format/'

test_mode = True

difference_days=1


#date_format='%Y%m%d'

current_date=datetime.today().strftime('%Y-%m-%d')

yester_date = (datetime.today() - timedelta(days = difference_days)).strftime('%Y-%m-%d')
