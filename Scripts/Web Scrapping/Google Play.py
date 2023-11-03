#!/usr/bin/env python
# coding: utf-8

from google_play_scraper import app
import pandas as pd
import pandahouse as ph
from clickhouse_driver import Client
from tqdm import tqdm

bundle_list = pd.read_csv('/home/v.roizen/scripts/parsing/rustore_bundles.csv')

bundle_list = list(set(bundle_list['bundle_id']))

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

colmn=['bundle_id','google_play_version']
df=pd.DataFrame(columns=colmn)

for i in tqdm(range(len(bundle_list))):
    try:
        result = app(
            bundle_list[i],
            lang='en', # defaults to 'en'
            country='us' # defaults to 'us'
        )
        google_play_version=result.get('version')
        bundle_id=bundle_list[i]
    except:
        google_play_version='App not found'
        bundle_id=bundle_list[i]
    
    row = [bundle_id, google_play_version]
    new_df = pd.DataFrame([row], columns=colmn)
    df = pd.concat([df, new_df], ignore_index = True)

df.to_csv('/home/v.roizen/scripts/parsing/google_play.csv')

