#!/usr/bin/env python

import json
from pathlib import Path

data   = json.loads(Path('json/data.json').read_text())
themes = json.loads(Path('cache/themes.json').read_text())['themes']

for i in range(len(data), len(themes)):
    dic = {}
    theme = themes[i]['theme']
    dic['Category'] = f'第{i + 1}回 {theme}'
    dic['Worlds'] = []
    for w in themes[i]['worlds']:
        dic2 = {}
        dic2['ID'] = w['worldId']
        dic2['Name'] = w['worldName']
        dic2['RecommendedCapacity'] = w['recommendedCapacity']
        dic2['Capacity'] = w['capacity']
        dic['Worlds'].append(dic2)
    data.append(dic)

Path('cache/data.json').write_text(json.dumps(data, indent=4, ensure_ascii=False))
