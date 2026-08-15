#!/usr/bin/env python

import json
from pathlib import Path

local_world_lists = json.loads(Path('data/world_list.json').read_text())
ivs_world_lists   = json.loads(Path('cache/themes.json').read_text())['themes']
new_world_lists   = []

for i in range(len(ivs_world_lists)):
    theme      = ivs_world_lists[i]['theme']
    category   = f'第{i + 1}回 {theme}'
    world_list = {}
    world_list['Category'] = category
    world_list['Worlds']   = []
    
    if (i < len(local_world_lists)) and (local_world_lists[i]['Category'] == category):
        for w in local_world_lists[i]['Worlds']:
            world = {}
            world['ID']   = w['ID']
            world['Name'] = w['Name']
            world_list['Worlds'].append(world)
    else:
        for w in ivs_world_lists[i]['worlds']:
            world = {}
            world['ID']   = w['worldId']
            world['Name'] = w['worldName']
            world_list['Worlds'].append(world)

    new_world_lists.append(world_list)

Path('data/world_list.json').write_text((json.dumps(new_world_lists, indent=2, ensure_ascii=False)))
