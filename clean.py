#!/usr/bin/python3

import pandas as pd
import json

filebase = 'data/fbpac-ads-en-US'

print(f'Reading file {filebase}.csv...', end='', flush=True)
df = pd.read_csv(filebase + '.csv')
print(' done')

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
           'listbuilding_fundraising_proba']

print('Keeping columns:')
for column in columns:
    print('\t', column)

# Reduce dataset
df = df[columns]

print("Removing HTML from 'message'")
# Remove HTML from 'message'
df['message'] = df['message'].str.replace('<[^<]+?>', '')

n = df.shape[0]

print("Parsing 'targets' column...", end='', flush=True)
# Parse the 'targets' column
targets = {
    'Gender': [''] * n,
    'Age': [''] * n,
    'Retargeting': [''] * n,
    'Interest': [''] * n,
    'Segment': [''] * n,
    'State': [''] * n,
    'List': [''] * n,
    'Engaged with Content': [''] * n,
    'Language': [''] * n,
    'Website': [''] * n,
    'City': [''] * n,
    'Activity on the Facebook Family': [''] * n,
    'MaxAge': [''] * n,
    'Like': [''] * n,
    'MinAge': [''] * n,
    'RegionTarget': [''] * n,
    'Agency': [''] * n
}

for i, target in enumerate(df['targets']):
    if pd.isna(target):
        continue
    data = json.loads(target)
    for datum in data:
        col = datum['target']
        # Region exists in both targets and entities
        if col == 'Region':
            col = 'RegionTarget'
        if 'segment' in datum:
            val = datum['segment']
        else:
            val = '1'
        targets[col][i] = val

target_df = pd.DataFrame.from_dict(targets)
print(' done')

print("Parsing 'entities' column...", end='', flush=True)
# Parse the 'entities' column
entity_types = {
    'Organization': [''] * n,
    'Event': [''] * n,
    'Law': [''] * n,
    'RegionEntity': [''] * n,
    'Group': [''] * n,
    'Location': [''] * n,
    'Facility': [''] * n,
    'Person': [''] * n
}

for i, entity in enumerate(df['entities']):
    if pd.isna(entity):
        continue
    data = json.loads(entity)
    for datum in data:
        col = datum['entity_type']
        if col == 'Region':
            col = 'RegionEntity'
        val = datum['entity']
        entity_types[col][i] = val

entity_df = pd.DataFrame.from_dict(entity_types)
print(' done')

# Combine original dataframe with newly created, parsed dataframes
df = pd.concat([df, target_df, entity_df], axis=1, sort=False)

# Remove parsed and unneeded columns
df.drop('targets', axis=1, inplace=True)
df.drop('entities', axis=1, inplace=True)
df.drop('Like', axis=1, inplace=True)

print('Saving cleaned data')
# Save cleaned data
df.to_csv(filebase + '-cleaned.csv', index=False)
