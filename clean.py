#!/usr/bin/python3

import pandas as pd

df = pd.read_csv('data/fbpac-ads-en-US.csv')

# Columns to keep
columns = ['political',
           'not_political',
           'title',
           'message',
           'created_at',
           'updated_at',
           'impressions',
           'political_probability',
           'targets',
           'advertiser',
           'entities',
           'lower_page',
           'paid_for_by',
           'targetedness',
           'listbuilding_fundraising_proba'
          ]

# Reduce dataset
df = df[columns]

# Remove HTML from 'message'
df['message'] = df['message'].str.replace('<[^<]+?>', '')
