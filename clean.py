#!/usr/bin/env python
# coding: utf-8

# In[3]:


#!/usr/bin/python3

import pandas as pd
import json


# In[4]:


filebase = 'data/fbpac-ads-en-US'

print(f'Reading file {filebase}.csv...', end='', flush=True)
df = pd.read_csv(filebase + '.csv')
print(' done')


# In[5]:


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


# In[6]:


# Reduce dataset
df = df[columns]

print("Removing HTML from 'message'")
# Remove HTML from 'message'
df['message'] = df['message'].str.replace('<[^<]+?>', '')


# In[7]:


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


# In[8]:


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


age_bins = {
    '13-17': [0] * n,
    '18-34': [0] * n,
    '35-49': [0] * n,
    '50-64': [0] * n,
    '65+': [0] * n
}


# In[9]:


# Combine original dataframe with newly created, parsed dataframes
df = pd.concat([df, target_df, entity_df], axis=1, sort=False)

age_ranges = {
    '13-17': {'min': 13, 'max': 17},
    '18-34': {'min': 18, 'max': 34},
    '35-49': {'min': 35, 'max': 49},
    '50-64': {'min': 50, 'max': 64},
    '65+': {'min': 65, 'max': 1000},
}

print('Moving ages into bins...', end='', flush=True)
for i, (min_age, max_age) in enumerate(zip(df['MinAge'], df['MaxAge'])):
    if pd.isna(min_age):
        min_age = 0
    if pd.isna(max_age):
        max_age = 1000
    try:
    	min_age = float(min_age)
    except ValueError:
        min_age = 0.0
    try:
    	max_age = float(max_age)
    except ValueError:
        max_age = 1000
    for key, val in age_ranges.items():
        if min_age <= val['max'] and max_age >= val['min']:
            age_bins[key][i] = 1
print(' Done')

df = pd.concat([df, pd.DataFrame.from_dict(age_bins)], axis=1, sort=False)

# Remove parsed and unneeded columns
df.drop('targets', axis=1, inplace=True)
df.drop('entities', axis=1, inplace=True)
df.drop('List', axis=1, inplace=True)
df.drop('Engaged with Content', axis=1, inplace=True)
df.drop('Age', axis=1, inplace=True)


# In[10]:


Created_AT_Year = [int(x[0:4]) for x in df.created_at]
df['Created_At_Year'] = Created_AT_Year

Created_AT_Month = [int(x[5:7]) for x in df.created_at]
df['Created_At_Month'] = Created_AT_Month

Updated_AT_Year = [int(x[0:4]) for x in df.updated_at]
df['Updated_At_Year'] = Updated_AT_Year

Updated_AT_Month = [int(x[5:7]) for x in df.updated_at]
df['Updated_At_Month'] = Updated_AT_Month

#df.drop(columns=['created_at', 'updated_at'], inplace=True)

df['lower_page'] = df['lower_page'].str.replace('https://www.facebook.com/', '')
df['lower_page'] = df['lower_page'].str.replace('/', '')


# In[11]:


political_probability = []
for prob in df['political_probability']:
    if pd.isna(prob):
        political_probability.append(prob)
    elif prob > 0.9:
        political_probability.append(8)
    elif prob > 0.80:
        political_probability.append(7)
    elif prob > 0.70:
        political_probability.append(6)
    elif prob > 0.60:
        political_probability.append(5)
    elif prob > 0.50:
        political_probability.append(4)
    elif prob > 0.40:
        political_probability.append(3)
    elif prob > 0.30:
        political_probability.append(2)
    elif prob > 0.20:
        political_probability.append(1)
    else:
        political_probability.append(0)

df['political_probability_int'] = political_probability


# In[12]:


political_probability = []
for prob in df['listbuilding_fundraising_proba']:
    if pd.isna(prob):
        political_probability.append(prob)
    elif prob > 0.9:
        political_probability.append(8)
    elif prob > 0.80:
        political_probability.append(7)
    elif prob > 0.70:
        political_probability.append(6)
    elif prob > 0.60:
        political_probability.append(5)
    elif prob > 0.50:
        political_probability.append(4)
    elif prob > 0.40:
        political_probability.append(3)
    elif prob > 0.30:
        political_probability.append(2)
    elif prob > 0.20:
        political_probability.append(1)
    else:
        political_probability.append(0)

df['fundraising_proba_int'] = political_probability


# In[13]:


print(df.shape)
df.head()


# In[14]:


print('Saving cleaned data')
# Save cleaned data
df.to_csv(filebase + '-cleaned.csv', index_label='id')


# In[ ]:
