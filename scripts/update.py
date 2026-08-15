#!/usr/bin/python

import requests
import json
from pathlib import Path

CACHE_SERVER_URL = 'http://localhost:8010'

local_world_lists = json.loads(Path('data/world_list.json').read_text())

for i in range(len(local_world_lists)):
    for j in range(len(local_world_lists[i]['Worlds'])):
        world_id   = local_world_lists[i]['Worlds'][j]['ID']
        world_name = local_world_lists[i]['Worlds'][j]['Name']

        if world_id is not None:
            response = requests.get(CACHE_SERVER_URL + f'/world/{world_id}/update')

            if response.status_code == 200:
                print(f'[GenkaiTourWorldListUpdater] OK   第{i+1}回-{j+1} {world_name}')
            elif response.status_code == 404:
                print(f'[GenkaiTourWorldListUpdater] Fail 第{i+1}回-{j+1} {world_name}')

        else:
            print(f'[GenkaiTourWorldListUpdater] Skip 第{i+1}回-{j+1} {world_name}')
